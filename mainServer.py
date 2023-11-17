import socket
import threading
import json,pickle

HEADER = 64
FORMAT = 'utf-8'


HOST = socket.gethostbyname(socket.gethostname())
PORT = 43432




DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
SHARE = "SHARE"


def serialize(data):
    # Input data is in any format
    # Convert it into a byte format using pickle and return it
    
    return pickle.dumps(data)



def deserialize(data):
    # Input data is in byte format
    # Convert it into a tuple and return it
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



class DATA:
    def __init__(self):
        self.Data = { 
        }
    def add_to_data(self,addr,file_name):
        if addr in self.Data:
            self.Data[addr].append(file_name)
        else:
            self.Data[addr] = [file_name]
    def get_data_by_addr(self,addr):
         if addr in self.Data:
            data_ = self.Data[addr]
            return data_
    def rm_addr(self,addr):
        del(self.Data[addr])
    def delete_data_by_addr(self,addr,file_name):
         if addr in self.Data:
            self.Data[addr].remove(file_name)
            if self.Data[addr] == []:
                del(self.Data[addr])
    def get_all_active_files(self):
        return self.Data
    
# class REQUEST_QUEUE:
#     def __init__(self):
#         self.Queue = []

    
    
class Server:
    def __init__(self):
        self.start()
        pass
    def discover(self):
        pass
    def receive_Data(self):
        pass
    def handle_connection(self,conn,addr):
        print (f"NEW CONNECTION {addr} connected.")
        connected = True
        while connected: 
            CODE = recv_FORMAT(conn)
            if CODE==TRANSFER:
                file_name = recv_FORMAT(conn)
                file_size = recv_FORMAT(conn)
                with open("./recive/"+file_name,"wb") as file:
                    c=0
                    print(f"{CODE}")
                    while c < int(file_size):
                        msg_length = conn.recv(HEADER).decode(FORMAT)
                        msg_length = int(msg_length)
                        data = conn.recv(msg_length)
                        if not (data):
                            break
                        print(f"{data}")
                        c+=len(data)
                    print(f"Transfer Complete")
            elif CODE == DISCONECT:
                #set connection to False
                print(f"[{addr}] DISCONECTED")
                connected=False
            elif CODE == REQUEST:
                # REQUEST 
                # receive the file_name with the addr of that file
                # add to the REQUEST_QUEUE (request_addr,receive_addr,file_name)
                
                
                pass
            elif CODE == DISCORVER:
                # DISCORVER
                # send to this connection the list if active files
                print(f"{addr} DISCORVER")
                send_FORMAT(conn,self.file_Data.get_all_active_files())
                
                #conn.send()
                
                
            else:
                # if notthing else to do it will check for request
                # if the request request_addr match this connection address send to this connection that request
                pass
            
        conn.close()
        
    def start(self):
        # Start a server on a new thread 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST,PORT))
        
        self.file_Data = DATA()
        self.REQUEST_QUEUE = []


        #--------------Add dummy data----------------------
        self.file_Data.add_to_data(('1.1.1.1',6702),"text.txt")
        self.file_Data.add_to_data(('1.1.1.1',6701),"text2.txt")   
        
        #-----------------------------------------------------
        
        self.server.listen()
        print(f"Listening at address {HOST}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn,addr),name=addr)
            thread.start()
            print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")


print("Starting the server")
newServer = Server()












#----------------------------------Just testing thing out-------------------------------

# REQUEST_QUEUE = [('request_addr','receive_addr','file_name')]
# if 'request_addr' in REQUEST_QUEUE[0]:
#     print('wow')


# file_Data = DATA() 

# file_Data.add_to_data(('1.1.1.1',6702),"text.txt")
# file_Data.add_to_data(('1.1.1.1',6701),"text2.txt")
# print(pickle.loads(pickle.dumps(file_Data.get_all_active_files())))