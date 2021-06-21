import socket 
import threading

IP = '127.0.0.1'
PORT = 3000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def client_things():
    while True:
        message = client.recv(1024).decode("ascii")
        print(message)
        if message == "connection successful":
            username = input("write down your username!")
            client.send(username.encode('ascii')) 
        if message == "connected":
            message = f'{username}: {input("")}'
            client.send(message.encode('ascii'))


thread_client = threading.Thread(target=client_things)
thread_client.start()
