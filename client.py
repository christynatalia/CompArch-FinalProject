import socket 
import threading

IP = '127.0.0.1'
PORT = 3000

username = input("write down your username!")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def usernameClient():
    while True:
        message = client.recv(1024).decode("ascii")
        #client.send(username.encode('ascii'))
        print(message)

def sendClient():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))



thread_user_client = threading.Thread(target=usernameClient)
thread_user_client.start()

thread_send_client = threading.Thread(target=sendClient)
thread_send_client.start()





