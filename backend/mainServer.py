import socket
import threading
import json,pickle

HEADER = 64
FORMAT = 'utf-8'



save_path = "./auth_DATA.txt"

DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"
REQUEST = "REQUEST"
DISCORVER = "DISCORVER"
ERROR = "ERROR"
PUBLISH = "PUBLISH"
UNPUBLISH = "UNPUBLISH"
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
    try:
        conn.send(send_length)
        conn.send(message)
    except:
        pass
    
    
def recv_FORMAT(conn):
    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
    except:
        return DISCONECT
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
    def rm_files_by_username(self,username):
        self.Data = {k: (i[0],i[1]) for k, i in self.Data.items() if username != i[0]}
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



class auth_DATA:
    def __init__(self,path):
        self.path = path
        self.Data = {
            #username : (password, active)
        }
        self.Data = self.load()

    def reg(self,username,password):
        if username in self.Data:
            return "This user already exist"
        else:
            self.Data[username] = (password,False)
            return "Succecfully added user"
    def auth(self,username,password):
        if username not in self.Data: 
            return "This user not exist"
        elif password == self.Data[username][0]:
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
            else:
                return {}  
    def get_active_user(self):
        return {k: (i[0],i[1]) for k, i in self.Data.items() if i[1] == True}
    def get_all(self):
        return self.Data
    def toggle_user(self,username):
        if username in self.Data:
            current_tuple = self.Data[username]
            updated_tuple = (current_tuple[0], not current_tuple[1])
            self.Data[username] = updated_tuple
    def rm_all(self):
        self.Data = {}
        
class Server:
    def __init__(self):
        self.file_Data = file_DATA()
        self.auth_Data = auth_DATA(save_path) 
        self.setHost()
    def setHost(self,host = socket.gethostbyname(socket.gethostname()),port = 54321):
        self.HOST = host
        self.PORT = port
    def handle_connection(self,conn,addr):
        print (f"NEW CONNECTION {addr} connected.")
        connected = True
        username = ""
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
                self.auth_Data.toggle_user(username)
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
            if CODE==PUBLISH:
                msg = recv_FORMAT(conn)
                #(addr,filename)
                print(f"{addr} PUBLISH {msg[1]}")
                self.file_Data.add_to_data(msg[0],msg[1],username)
                # add to the data_file
            if CODE == UNPUBLISH:
                msg = recv_FORMAT(conn)
                #(addr,filename)
                print(f"{addr} UNPUBLISH {msg[1]}")
                send_FORMAT(conn,self.file_Data.delete_files_by_addr(msg[0],msg[1]))
                # add to the data_file  
            elif CODE == DISCONECT:
                # set connection to False
                connected=False
            elif CODE == DISCORVER:
                # DISCORVER
                # send to this connection the list if active files
                filter = recv_FORMAT(conn)
                print(f"{addr} DISCORVER {filter}")
                if (filter):
                    send_FORMAT(conn,self.file_Data.get_data_by_file_name(filter))
                else:
                    send_FORMAT(conn,self.file_Data.get_all_active_files())
                
        print(f"[{addr}] DISCONECTED")
        # delete the share file of that addr
        self.file_Data.rm_files_by_username(username)
        self.auth_Data.toggle_user(username)
        conn.close()
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST,self.PORT))
        
        self.thread = threading.Thread(target=self.server_listener,name="Server listener thread")
        self.thread.start()
        
    def server_listener(self):
        # Start the server on a new thread 
        self.server.listen()
        print(f"Listening at address {self.HOST} : {self.PORT}")
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_connection, args=(conn,addr),name=addr)
                thread.start()
                print(f"[ACTIVE CONNECTONS] {threading.active_count() - 2}")
        except:
            print("The server is close")
        
    def get_active_connection(self):
        return self.auth_Data.get_active_user()
    def get_share_files(self,filter):
        if (filter):
            return self.file_Data.get_data_by_file_name(filter)
        else:
            return self.file_Data.get_all_active_files()
    def shutdown(self):
        self.server.close()
# print("Starting the server")
# server = Server()
# server.start()
# #Keep the main not dying
# input()
# #print(newServer.get_active_connection())
# server.shutdown()





#----------------------------------Just testing thing out-------------------------------

# REQUEST_QUEUE = [('request_addr','receive_addr','file_name')]
# if 'request_addr' in REQUEST_QUEUE[0]:
#     print('wow')


# file_Data = file_DATA() 

# file_Data.add_to_data(('1.1.1.1',6702),"text.txt","me")
# file_Data.add_to_data(('1.1.1.1',6702),"text3.txt")
# file_Data.add_to_data(('1.1.1.1',6701),"text2.txt","b")
# file_Data.add_to_data(('1.1.1.1',6701),"text.txt")
# print(file_Data.get_all_active_files())
# file_Data.rm_files_by_username("me")
# file_Data.rm_files_by_username("")


# print(pickle.loads(pickle.dumps(file_Data.get_all_active_files())))



# auth_Data = auth_DATA(save_path)
# print(auth_Data.reg("hello","hello"))
# print(auth_Data.reg("admin","admin"))
# print(auth_Data.reg("123","123"))
# auth_Data.reg("Tuan","321")
# auth_Data.save()

# data = {('1.1.1.1', 6702): ('me', ['text.txt', 'text3.txt']), ('1.1.1.1', 6701): ('b', ['text2.txt', 'text.txt'])}
# print ([[k, i[0],i[1]] for k, i in data.items()[2]])