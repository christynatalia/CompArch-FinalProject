import socket 
import threading

IP = '127.0.0.1'
PORT = 3000
HEADER_LENGTH = 10

username = input("Enter your username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def usernameClient():
    while True:
        try:
            try:
                messageHeader = client.recv(HEADER_LENGTH)
                if not len(messageHeader):
                    return False
                
                messageLength = int(messageHeader.decode('ascii').strip())
                message = client.recv(messageLength).decode('ascii')
                
            except:
                message=client.recv(1024).decode('ascii')
            if message == 'connection successful':
                client.send(username.encode('ascii'))
            else:
                print(message)
        
        except:
            client.close()
            break

def sendClient():
    while True:
        message = f'{username}: {input("")}'
        message = message.encode('ascii')
        messageHeader = f'{len(message):<{10}}'.encode('ascii')
        #client.send(message.encode('ascii'))
        client.send(messageHeader + message)



thread_user_client = threading.Thread(target=usernameClient)
thread_user_client.start()

thread_send_client = threading.Thread(target=sendClient)
thread_send_client.start()





