import socket
import os

HEADER = 64
FORMAT = 'utf-8'

HOST = "10.230.93.136"
PORT = 5554

DISCONECT = "DISCONECT"
TRANSFER = "TRANSFER FILE"



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))


def send_FORMAT(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    

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
            client.sendall(data)
            c+=len(data)
    print("Transfer Complete")
    
    
def disconect():
    client.send(DISCONECT.encode())
    print(f"DISCONECT")
    client.close()
    
    
send_file()
disconect()