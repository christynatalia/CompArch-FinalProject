import socket
import threading


IP = '127.0.0.1'
PORT = 3000

HEADER_LENGTH = 10

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((IP, PORT))

# Only listen for 5 connections
# Chnage to different number according your needs
serverSocket.listen(5)

listOfClients = []
usernames = []

print(f'Server is running on {IP}:{PORT}')


def clientThread(client):
    while True:
        try:
            messageHeader = client.recv(HEADER_LENGTH)
            if not len(messageHeader):
                return False
            
            messageLength = int(messageHeader.decode('ascii').strip())
            message = client.recv(messageLength)
            broadcast(message)
            
        except:
            index = listOfClients.index(client)
            listOfClients.remove(client)
            client.close()
            
            username = usernames[index]
            broadcast(f'{username} has left the chat room!'.encode('ascii'))
            usernames.remove(username)
            
            break
        
    

def broadcast(message):
    for client in listOfClients:
        messageHeader = f'{len(message):<{HEADER_LENGTH}}'.encode('ascii')
        client.send(messageHeader + message)
    
    

while True:
    print("Waiting for connection ...")
    
    client, address = serverSocket.accept()
    print(f'{str(address)} create new connection!')
    
    # Make sure to change checking on the client side
    # Same with this one
    message = 'username?'.encode('ascii')
    messageHeader = f'{len(message):<{HEADER_LENGTH}}'.encode('ascii')
    client.send(messageHeader + message)
    
    username = client.recv(1024)
    usernames.append(username)
    listOfClients.append(client)
    
    broadcast(f'{username} has enter the chat room!'.encode('ascii'))
    
    message = 'You are connected to the server!'.encode('ascii')
    messageHeader = f'{len(message):<{HEADER_LENGTH}}'.encode('ascii')
    client.send(messageHeader + message)
    print(username, "is", f'{str(address)}')
    
    threading._start_new_thread(clientThread, (client,))