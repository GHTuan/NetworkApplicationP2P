import socket
import threading

HEADER = 64
FORMAT = 'utf-8'


HOST = socket.gethostbyname(socket.gethostname())
PORT = 43432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))


DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
SHARE = "SHARE"

def recv_FORMAT(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        return conn.recv(msg_length).decode(FORMAT)

def send_FORMAT(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)



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

    
    


def discover():
    pass

def receive_Data():
    pass




def handle_connection(conn,addr):
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
                print("Transfer Complete")
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
            
            
            pass
        else:
            # if notthing else to do it will check for request
            # if the request request_addr match this connection address send to this connection that request
            pass
        
    conn.close()
          
    
          
          
          
                  
def start():
    file_Data = DATA()
    REQUEST_QUEUE = []

    
    
    
    
    server.listen()
    print(f"Listening at address {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_connection, args=(conn,addr),name=addr)
        thread.start()
        print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")

print("Starting the server")
#start()



REQUEST_QUEUE = [('request_addr','receive_addr','file_name')]
if 'request_addr' in REQUEST_QUEUE[0]:
    print('wow')



# file_Data = DATA() 
# print(file_Data.get_data_by_addr(('1.1.1.1',6702)))

# file_Data.add_to_data(('1.1.1.1',6702),"text.txt")
# file_Data.add_to_data(('1.1.1.1',6701),"text2.txt")
# print(file_Data.get_all_active_files())