#Establishes the connection to the main server (hard code the HOST and PORT) (reference: Sender.py) 
#After establishing the connection to the main server, setup your own server using your local IP and on port 43432.
#Requrement: Your connection to the main server and your own server must run on different thread
#            The server must be able to handle multiple connection (reference: Receive.py) 

import socket
import os
import threading

HEADER = 64
FORMAT = 'utf-8'

HOST = "26.75.111.47"  # change to your Local IP
PORT = 43432

DISCONNECT = "DISCONNECT"
TRANSFER = "TRANSFER FILE"


def connectServer():
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.connect((HOST, PORT)) # of server

    def send_FORMAT(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        peer.send(send_length)
        peer.send(message)

    def disconnect():
        send_FORMAT(DISCONNECT)
        print(f"DISCONNECT")
        peer.close()

    def send_file(file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        send_FORMAT(TRANSFER)
        send_FORMAT(file_name)
        send_FORMAT(str(file_size))

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                peer.send(data)
                data = file.read(1024)

        print("File transfer complete.")

    send_file('path/to/your/file.txt')  # Replace with the path to your file
    disconnect()


def createServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print('Server(Peer) is listening on {}:{}'.format(HOST, PORT))

    conn, addr = server.accept()
    print('Connected to {}:{}'.format(addr[0], addr[1]))

    def recv_FORMAT(conn):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            return conn.recv(msg_length).decode(FORMAT)

    #def handle_sender(conn, addr):
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
                        break
                    file.write(data)
                    c += len(data)

                print("Transfer complete")

        elif CODE == DISCONNECT:
            print(f"[{addr}] DISCONNECTED")
            connected = False

    conn.close()


# Sử dụng threading để chạy cả máy chủ và máy khách cùng một lúc
server_thread = threading.Thread(target=createServer)
server_thread.start()

client_thread = threading.Thread(target=connectServer)
client_thread.start()