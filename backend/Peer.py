#Establishes the connection to the main server (hard code the HOST and PORT) (reference: Sender.py) 
#After establishing the connection to the main server, setup your own server using your local IP and on port 43432.
#Requrement: Your connection to the main server and your own server must run on different thread
#            The server must be able to handle multiple connection (reference: Receive.py) 


# Note that the address are in tuple format: (string,number)

# UPDATE 
# update on the function send_FORMAT() and recv_FORMAT()
# now the function can send any format use it to your advantage 



import socket
import os
import threading

import pickle

HEADER = 64
FORMAT = 'utf-8'

SERVER_HOST = "192.168.62.119"
SERVER_PORT = 43432

#HOST = socket.gethostbyname(socket.gethostname())  # change to your Local IP
HOST = "192.168.62.119"
PORT = 12345

DISCONNECT = "DISCONNECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
PUBLISH = "PUBLISH"
UNPUBLISH = "UNPUBLISH"
SUCCESS = "SUCCESS"
FAIL = "FAILED"
NOTFOUND = "FILE NOT FOUND"


def serialize(data):
    # Input data is in any format
    # Convert it into a byte format using pickle and return it
    
    return pickle.dumps(data)
    



def deserialize(data):
    # Input data is in byte format
    # Convert the data back to it format and return it
    return pickle.loads(data)

        


def send_FORMAT(conn,msg):
    message = serialize(msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    
    
def recv_FORMAT(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        data = deserialize(conn.recv(msg_length))
        return data


class Peer1:
    def  __init__(self):
        self.OPEN_SERVER=False
        self.connect_To_MainServer()
        self.allowPath=[]
        
    def connect_To_MainServer(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((SERVER_HOST, SERVER_PORT)) # of server
            print(f"Connection establishes")
        except:
            print(f"The server is offline")   

    def login(self,username="defauft",password="defauft"):
        send_FORMAT(self.conn,(username,password))
        r = recv_FORMAT(self.conn)
        return r     
    def startServer(self):
        # This is the server on your computer that is responsible receiving the file
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        print("Starting your sharing server")        
        self.thread = threading.Thread(target=self.server_listener,name="Server listener thread")
        self.thread.start()
       
    def server_listener(self):
        self.server.listen(1)
        print('Server(Peer) is listening on {}:{}'.format(HOST, PORT))
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_peer_connection, args=(conn,addr))
                thread.start()
                print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")
        except:
            print("Your sharing server is shutdown")
    
    def OFF(self):
        # turn off the connecion to the main server and your receive server (you might need to change some other starting function)
        if(self.OPEN_SERVER):
            self.server.close()
            self.OPEN_SERVER=False
        self.send_DISCONNECT()

    def send_DISCONNECT(self):
        send_FORMAT(self.conn,DISCONNECT)
        print(f"DISCONNECT")
        self.conn.close()
   
    def send_PUBLISH(self,file_name):
        if not self.OPEN_SERVER:
            self.OPEN_SERVER = True
            self.startServer()
        send_FORMAT(self.conn,PUBLISH)
        # send PUBLISH
        # this just need to inform the server the file it has
        # and the addr this peer have open the server on
        send_FORMAT(self.conn,((HOST, PORT),file_name))
        self.allowPath.append(file_name)
    
    def send_UMPUBLISH(self,file_name):
        send_FORMAT(self.conn,UNPUBLISH)
        
        send_FORMAT(self.conn,((HOST, PORT),file_name))
        r = recv_FORMAT(self.conn)
        if r == SUCCESS:
            try:
                self.allowPath.remove(file_name)
            except:
                return "This file is not currenly sharing"
        return r
        
    def send_DISCOVER(self,file=""):
        send_FORMAT(self.conn,DISCORVER)
        send_FORMAT(self.conn,file)
        # send DISCOVER
        # you are about to receive a msg from the server
        # the msg in a tuple contain all the info about file the server has
        # design a way to receive that msg
        
        data = recv_FORMAT(self.conn)
        print (f"{data}")
    #P2P Operation   
    def send_file(self,conn,file_path):
        
        file_path = "./send/"+file_path
        file_size = os.path.getsize(file_path)

        send_FORMAT(conn,str(file_size))

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                data = file.read(1024)
            print("File transfer complete.")
          
    def fetch(self,addr,file_name):
        # for sending multiple request when calling this function we should use threading when calling fetch
        
        # send REQUEST
        # you need to change the parameter of this function for what needed
        # connent to the other peer and send a REQUEST the REQUEST should contain the file_name it wanted
        # after REQUEST you will be inform by a CODE [NOT FOUND,TRANSFER]
        # if CODE is TRANSFER then there will be a files send to you, receive that file reference:recv_file
        # disconect from this connection
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(addr)
        except:
            return "The request server is offline"
        
        send_FORMAT(conn,REQUEST)
        send_FORMAT(conn,file_name)
        r = recv_FORMAT(conn)
        if r == NOTFOUND:
            send_FORMAT(conn,DISCONNECT)
            return "This file is not avilable"
        else:
            file_size = recv_FORMAT(conn)
            file_path = "./receive/" + file_name

            with open(file_path, "wb") as file:
                c = 0
                while c < int(file_size):
                    data = conn.recv(1024)
                    if not data:
                        #the sender disconnected
                        conn.close
                    file.write(data)
                    c += len(data)

            print("Transfer complete")
            
            send_FORMAT(conn,DISCONNECT)
        
        
    def handle_peer_connection(self,conn,addr):
        print(f"NEW CONNECTION {addr} connected.")
        connected = True
        while connected:
            CODE = recv_FORMAT(conn)
            if CODE == REQUEST:
                # locate the file the request needed
                # if not found send to this connection the NOTFOUND code
                # if found the file send the TRANSFER code then send the file to this connection
                # reference: send_file()
                file_name = recv_FORMAT(conn)
                print(f"Sending {file_name}")
                if file_name in self.allowPath:
                    send_FORMAT(conn,TRANSFER)
                    self.send_file(conn,file_name)
                else: 
                    send_FORMAT(conn,NOTFOUND)
                 
            elif CODE == DISCONNECT:
                print(f"[{addr}] DISCONNECTED")
                connected = False
        conn.close()
    
# Testing Part
# Run the mainServer.py First


peer1 = Peer()
while True:
    print("Testing username: 123, password:123")
    username=input("Username:")
    password=input("Password:")
    if peer1.login(username,password) == "Login in success":
        break
    else:
        print("Wrong!")
running = True
while running:
    print("""
          Choose:
          1. PUBLISH
          2. UNPUBLISH
          3. DISCORVER
          4. DISCONECT
          5. FETCH
          6. OFF
          """)
    op = int(input("ops:"))
    if op == 1:
        file_name = input("Ten File: ")
        peer1.send_PUBLISH(file_name)
    elif op == 2:    
        file_name = input("Ten File: ")
        peer1.send_UNPUBLISH(file_name)
    elif op == 3: 
        filter = input("Tim kiem (de trong de tim kiem tat ca): ")
        if filter:
            peer1.send_DISCOVER(filter)
        else :
            peer1.send_DISCOVER()
    elif op == 4: 
        running = False
        peer1.send_DISCONNECT()
        
    elif op == 5: 
        ip = input("IP:")
        port = int(input("PORT:"))
        file_name = input("Ten file:")
        print(peer1.fetch((ip,port),file_name))
    elif op == 6: 
        running = False
        peer1.OFF()
    else: 
        running = False
        print("unexpected input, OFF")
        peer1.OFF()
        

# add to function you want to test here
#peer1.send_DISCONNECT()

