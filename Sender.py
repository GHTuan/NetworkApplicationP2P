import socket
import os

HEADER = 64
FORMAT = 'utf-8'

HOST = "10.230.93.136"
PORT = 43432

DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"



sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect((HOST,PORT))


def send_FORMAT(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sender.send(send_length)
    sender.send(message)
    
def send_file():
    
    file_name = input("File Name: ")
    file_size = os.path.getsize("./send/"+file_name)
    
    send_FORMAT(TRANSFER)
    
    send_FORMAT(file_name)
    
    send_FORMAT(str(file_size))
    
    with open("./send/"+file_name,"rb") as file:
        c=0
        
        while c <= file_size:
            data = file.read(1024)
            if not (data):
                break
            sender.sendall(data)
            c+=len(data)
    print("Transfer Complete")
    
    
def disconect():
    send_FORMAT(DISCONECT)
    print(f"DISCONECT")
    sender.close()
    
    
send_file()
disconect()