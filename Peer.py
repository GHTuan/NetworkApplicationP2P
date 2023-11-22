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

SERVER_HOST = "26.75.111.47"
SERVER_PORT = 43432

HOST = socket.gethostbyname(socket.gethostname())  # change to your Local IP
PORT = 12345

DISCONNECT = "DISCONNECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
SHARE = "SHARE"
UNSHARE = "STOPSHARING"
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


class Peer:
    def  __init__(self):
        self.OPEN_SERVER=False
        self.connect_To_MainServer()
        
       
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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)
        print('Server(Peer) is listening on {}:{}'.format(HOST, PORT))
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_peer_connection, args=(conn,addr))
            thread.start()
            print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")

    def send_DISCONNECT(self):
        send_FORMAT(DISCONNECT)
        print(f"DISCONNECT")
        self.conn.close()
   
    def send_SHARE(self,file_name):
        if not self.OPEN_SERVER:
            self.OPEN_SERVER = True
            server_thread = threading.Thread(target=self.startServer)
            server_thread.start()
        send_FORMAT(self.conn,SHARE)
        # send SHARE
        # this just need to inform the server the file it has
        # and the addr this peer have open the server on
        send_FORMAT(self.conn,((HOST, PORT),file_name))
    
    def send_UNSHARE(self,file_name):
        send_FORMAT(self.conn,UNSHARE)
        
        send_FORMAT(self.conn,((HOST, PORT),file_name))
        r = recv_FORMAT(self.conn)
        return r
        
    def send_DISCOVER(self,file=""):
        send_FORMAT(self.conn,DISCORVER)
        send_FORMAT(self.conn,'')
        # send DISCOVER
        # you are about to receive a msg from the server
        # the msg in a tuple contain all the info about file the server has
        # design a way to receive that msg
        
        data = recv_FORMAT(self.conn)
        print (f"{data}")
        pass
    def OFF(self):
        # you don't need to do this part yet
        # try to turn off the connecion to the main server and your receive server (you might need to change some other starting function)
        
        # TODO  
        pass
    def handle_request_from_mainServer(self):
        #will be a new thread to handle the server request
        connected = True
        while connected:
            CODE = recv_FORMAT(self.conn)    
            if CODE == REQUEST:
                # receive REQUEST
                # you are about to receive a msg from the server
                # the msg in a tuple contain (request_addr,receive_addr,file_name)
                # next up, connect to the server with that receive_addr you just got
                # use the send_file() function to send the file to that connection you just made
                # disconect from that connection.
                
                # TODO
                
                # You can make new function for better visualization
                
                pass
            else:   
                
                pass
                
    #P2P Operation   
    def send_file(self,file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        send_FORMAT(TRANSFER)
        send_FORMAT(file_name)
        send_FORMAT(str(file_size))

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                self.conn.send(data)
                data = file.read(1024)
            print("File transfer complete.")
    
    def recv_file(self,conn):
        file_name = recv_FORMAT(conn)
        file_size = recv_FORMAT(conn)
        file_path = "./recive/" + file_name

        with open(file_path, "wb") as file:
            c = 0
            while c < int(file_size):
                data = conn.recv(1024)
                if not data:
                    #the sender disconnected
                    connected = False
                file.write(data)
                c += len(data)

            print("Transfer complete")
          
    def fetch(self):
        # for sending multiple request when calling this function we should use threading 
        
        # send REQUEST
        # you need to change the parameter of this function for what needed
        # connent to the other peer and send a REQUEST the REQUEST should contain the file_name it wanted
        # after REQUEST you will be inform by a CODE [NOT FOUND,TRANSFER]
        # if CODE is TRANSFER then there will be a files send to you, receive that file reference:recv_file
        # disconect from this connection
        
        # TODO
        
        # send_FORMAT(self. ,REQUEST)
        
        pass
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
                
                
                # TODO
                pass 


            elif CODE == DISCONNECT:
                print(f"[{addr}] DISCONNECTED")
                connected = False
        conn.close()
    
        
# Testing Part
# you need to run a dummy server to test 
peer1 = Peer()
while True:
    username=input("Username:")
    password=input("Password:")
    if peer1.login(username,password) == "Login in success":
        break
    else:
        print("Wrong!")
input()
peer1.send_SHARE("Hehe.txt")
peer1.send_SHARE("Hehe2.txt")
input()
peer1.send_DISCOVER()
input()
print(peer1.send_UNSHARE("Hehe.txt"))
peer1.send_DISCOVER()
input()
print(peer1.send_UNSHARE("Hehe.txt"))
peer1.send_DISCOVER()
input()

# add to function you want to test here
#peer1.send_DISCONNECT()
