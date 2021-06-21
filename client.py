import socket 
import threading

IP = '127.0.0.1'
PORT = 3000


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

message = client.recv(1024).decode("utf-8")
print(message)