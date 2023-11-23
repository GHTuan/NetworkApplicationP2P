import socket
import threading
import json,pickle

HEADER = 64
FORMAT = 'utf-8'

HOST = socket.gethostbyname(socket.gethostname())
# HOST = "192.168.100.3"
PORT = 43432


DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
SHARE = "SHARE"
UNSHARE = "STOPSHARING"
SUCCESS = "SUCCESS"
FAIL = "FAILED"


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




class file_DATA:
    def __init__(self):
        self.Data = { 
            #string
            #list             
        }
    def add_to_data(self,addr,file_name,username="User"):
        if addr in self.Data:
            self.Data[addr][1].append(file_name)
        else:
            self.Data[addr] = (username,[file_name])
    def get_data_by_addr(self,addr):
         if addr in self.Data:
            data_ = self.Data[addr]
            return data_
    def rm_addr(self,addr):
        if addr in self.Data:
            del(self.Data[addr])
    def delete_files_by_addr(self,addr,file_name):
        if addr in self.Data:
            try: 
                (self.Data[addr][1].remove(file_name))
            except:
                return FAIL
            if self.Data[addr][1] == []:
                del(self.Data[addr])
        else:
            return FAIL
        return SUCCESS
        
    def get_all_active_files(self):
        return self.Data
    def get_data_by_file_name(self,file_name):
        return {k: (i[0],[file_name]) for k, i in self.Data.items() if file_name in i[1]}

save_path = "./auth_DATA.txt"


class auth_DATA:
    def __init__(self,path):
        self.path = path
        self.Data = {
        }
        self.Data = self.load()
        
        
    def reg(self,username,password):
        if username in self.Data:
            return "This user already exist"
        else:
            self.Data[username] = password
            return "Succecfully added user"
    def auth(self,username,password):
        if username not in self.Data: 
            return "This user not exist"
        elif password == self.Data[username]:
            return "Login in success"
        else: return "Wrong password" 
    def save(self):
        with open(self.path,"wb") as files:
            data = serialize(self.Data)
            files.write(data)
    def load(self):
        with open(self.path,"rb") as files:
            data = files.read()
            if data:
                return deserialize(data)    
    def get(self):
        return self.Data
        
class Server:
    def __init__(self):
        self.file_Data = file_DATA()
        self.auth_Data = auth_DATA(save_path)

        #--------------Add dummy data----------------------
        # self.file_Data.add_to_data(('1.1.1.1',6702),"text.txt")
        # self.file_Data.add_to_data(('1.1.1.1',6701),"text2.txt")  
        # self.file_Data.add_to_data(('1.1.1.1',6702),"text2.txt")  
        
        #-----------------------------------------------------
        self.start()
        
    def handle_connection(self,conn,addr):
        print (f"NEW CONNECTION {addr} connected.")
        connected = True
        
        auth=False
        while not auth:
            auth_info = recv_FORMAT(conn)
            #(username,password)
            try:
                r = self.auth_Data.auth(auth_info[0],auth_info[1])
            except:
                #wrong format or user disconnected via 
                connected=False
                break
            send_FORMAT(conn,r)
            if r == "Login in success" :
                username = auth_info[0]
                break
        while connected: 
            try:
                CODE = recv_FORMAT(conn)
            except:
                # The connection was forcefully shutdown
                connected = False
                break
            
            if not CODE:
                connected = False
                break
            
            if CODE==SHARE:
                msg = recv_FORMAT(conn)
                #(addr,filename)
                self.file_Data.add_to_data(msg[0],msg[1],username)
                # add to the data_file
            if CODE == UNSHARE:
                msg = recv_FORMAT(conn)
                #(addr,filename)
                send_FORMAT(conn,self.file_Data.delete_files_by_addr(msg[0],msg[1]))
                # add to the data_file  
            elif CODE == DISCONECT:
                
                # set connection to False
                connected=False
                # delete the share file of that addr
                share_server_addr = recv_FORMAT(conn)
                self.file_Data.rm_addr(addr)
            elif CODE == DISCORVER:
                # DISCORVER
                # send to this connection the list if active files
                print(f"{addr} DISCORVER")
                filter = recv_FORMAT(conn)
                if (filter):
                    send_FORMAT(conn,self.file_Data.get_data_by_file_name(filter))
                else:
                    send_FORMAT(conn,self.file_Data.get_all_active_files())
                
        print(f"[{addr}] DISCONECTED")
        conn.close()
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST,PORT))
        
        self.thread = threading.Thread(target=self.server_listener,name="Server listener thread")
        self.thread.start()
        
    def server_listener(self):
        # Start the server on a new thread 
        
        self.server.listen()
        print(f"Listening at address {HOST}")
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_connection, args=(conn,addr),name=addr)
                thread.start()
                print(f"[ACTIVE CONNECTONS] {threading.active_count() - 2}")
        except:
            print("The server is close")
        
    def get_active_connection(self):
        return [thread.name for thread in threading.enumerate()]
    def get_share_files(self):
        return self.file_Data.get_all_active_files()
    def shutdown(self):
        self.server.close()
print("Starting the server")
server = Server()
#Keep the main not dying
input()
#print(newServer.get_active_connection())
server.shutdown()





#----------------------------------Just testing thing out-------------------------------

# REQUEST_QUEUE = [('request_addr','receive_addr','file_name')]
# if 'request_addr' in REQUEST_QUEUE[0]:
#     print('wow')


# file_Data = file_DATA() 

# file_Data.add_to_data(('1.1.1.1',6702),"text.txt")
# file_Data.add_to_data(('1.1.1.1',6702),"text3.txt")
# file_Data.add_to_data(('1.1.1.1',6701),"text2.txt","b")
# file_Data.add_to_data(('1.1.1.1',6701),"text.txt")
# print(file_Data.delete_files_by_addr(('1.1.1.1',6702),"text.txt"))
# print(file_Data.delete_files_by_addr(('1.1.1.1',6702),"text.txt"))

# print(pickle.loads(pickle.dumps(file_Data.get_all_active_files())))
# print(file_Data.get_data_by_file_name("text.txt"))


# auth_Data = auth_DATA(save_path)
# print(auth_Data.reg("hello","hello"))
# print(auth_Data.reg("admin","admin"))
# print(auth_Data.reg("123","123"))
# print(auth_Data.get())
# auth_Data.save()
