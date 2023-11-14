import socket
import threading

HEADER = 64
FORMAT = 'utf-8'


HOST = socket.gethostbyname(socket.gethostname())
PORT = 43432

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