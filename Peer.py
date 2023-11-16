#Establishes the connection to the main server (hard code the HOST and PORT) (reference: Sender.py) 
#After establishing the connection to the main server, setup your own server using your local IP and on port 43432.
#Requrement: Your connection to the main server and your own server must run on different thread
#            The server must be able to handle multiple connection (reference: Receive.py) 


# Note that the address are in tuple format: (string,number)


import socket
import os
import threading

HEADER = 64
FORMAT = 'utf-8'

SERVER_HOST = "26.75.111.47"
SERVER_PORT = 12345

HOST = socket.gethostbyname(socket.gethostname())  # change to your Local IP
PORT = 43432

DISCONNECT = "DISCONNECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
SHARE = "SHARE"

def send_FORMAT(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    
    
def recv_FORMAT(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        return conn.recv(msg_length).decode(FORMAT)


class Peer:
    def  __init__(self):
        self.connect_To_MainServer()
        self.OPEN_SERVER=False
       
    def connect_To_MainServer(self):
        try:
            self.peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer.connect((SERVER_HOST, SERVER_PORT)) # of server
            print(f"Connection establishes")
        except:
            print(f"The server is offline")   

    def handle_connection(self,conn,addr):
        print(f"NEW CONNECTION {addr} connected.")
        connected = True
        while connected:
            CODE = recv_FORMAT(conn)
            if CODE == TRANSFER:
                file_name = recv_FORMAT(conn)
                file_size = recv_FORMAT(conn)
                file_path = "./recive/" + file_name

                with open(file_path, "wb") as file:
                    c = 0
                    print(f"{CODE}")
                    while c < int(file_size):
                        data = conn.recv(1024)
                        if not data:
                            #the sender disconnected
                            connected = False
                        file.write(data)
                        c += len(data)

                    print("Transfer complete")

            elif CODE == DISCONNECT:
                print(f"[{addr}] DISCONNECTED")
                connected = False
        conn.close()
            
    def startServer(self):
        # This is the server on your computer that is responsible receiving the file
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)
        print('Server(Peer) is listening on {}:{}'.format(HOST, PORT))
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn,addr))
            thread.start()
            print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")

    def send_DISCONNECT(self):
        send_FORMAT(DISCONNECT)
        print(f"DISCONNECT")
        self.peer.close()

    def send_file(self,file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        send_FORMAT(TRANSFER)
        send_FORMAT(file_name)
        send_FORMAT(str(file_size))

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                self.peer.send(data)
                data = file.read(1024)

            print("File transfer complete.")
    def send_REQUEST(self):
        #you will need to have a server to receive something
        if not self.OPEN_SERVER:
            self.OPEN_SERVER = True
            server_thread = threading.Thread(target=self.startServer)
            server_thread.start()
        send_FORMAT(self.peer ,REQUEST)
        # send REQUEST
        # you may need to change the parameter of this function for what needed
        # send a REQUEST combine in one-line contain the following:
        # request_addr : this is the address the file is sending from 
        # receive_addr : this is the address of your server 
        # file_name: string format
        # Note that since REQUEST is a tuple (request_addr,receive_addr,file_name) you can't use send_FORMAT() 
        
        # TODO
        
        pass
    def send_SHARE(self,file_name):
        send_FORMAT(self.peer,SHARE)
        # send SHARE
        # this just need to inform the server the file it has
        send_FORMAT(file_name)
    
    def send_DISCOVER(self):
        send_FORMAT(self.peer,DISCORVER)
        # send DISCOVER
        # you are about to receive a msg from the server
        # the msg in a tuple contain all the info about file the server has
        # design a way to receive that msg
        # Note that since msg receive is a tuple you can't get it using recv_FORMAT()
        
        # TODO
        
        pass
    def OFF(self):
        # you don't need to do this part yet
        # try to turn off the connecion to the main server and your receive server (you might need to change some other starting function)
        
        # TODO  
        pass

    def handle_request(self):
        #will be a new thread to handle the server request
        connected = True
        while connected:
            CODE = recv_FORMAT(self.peer)    
            if CODE == REQUEST:
                # receive REQUEST
                # you are about to receive a msg from the server
                # the msg in a tuple contain (request_addr,receive_addr,file_name)
                # like the send_DISCOVER() your job is to retrive that msg
                # next up, connect to the server with that receive_addr you just got
                # use the send_file() function to send the file to that connection you just made
                # disconect from that connection.
                
                # TODO
                
                # You can make new function for better visualization
                
                pass
            else:   
                
                pass

        
        
# Testing Part
# you need to run a dummy server to test 
peer1 = Peer()
# add to function you want to test here
#peer1.send_DISCONNECT()
