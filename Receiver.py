import socket
import threading

HEADER = 64
FORMAT = 'utf-8'


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5554

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind((HOST,PORT))


DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"


def recv_FORMAT(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        return conn.recv(msg_length).decode(FORMAT)
    

def handle_sender(conn,addr):
    print (f"NEW CONNECTION {addr} connected.")
    
    connected = True
    while connected: 
        CODE = recv_FORMAT(conn)
        if CODE==TRANSFER:
            file_name = recv_FORMAT(conn)
            print(f"{file_name}")
            file_size = recv_FORMAT(conn)
            print(f"{file_size}")
            
            with open("./recive/"+file_name,"wb") as file:
                c=0
                
                while c <= int(file_size):
                    data = conn.recv(1024)
                    if not (data):
                        break
                    file.write(data)
                    c+=len(data)
                print("Transfer Complete")
            
        elif CODE == DISCONECT:
            print(f"[{addr}] DISCONECTED")
            connected=False
    conn.close()
                  
def start():
    receiver.listen()
    print(f"Listening at address {HOST}")
    while True:
        conn, addr = receiver.accept()
        thread = threading.Thread(target=handle_sender, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTONS] {threading.active_count() - 1}")

print("Starting the receiver")
start()



   
    