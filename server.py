import socket
import threading


IP = '127.0.0.1'
PORT = 3000

HEADER_LEGNTH = 256

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((IP, PORT))

# Only listen for 5 connections
# Chnage to different number according your needs
serverSocket.listen(5)

listOfClients = []
usernames = []

print(f'Waiting for connections on {IP}:{PORT}')

def clientThread(client):
    while True:
        try:
            message = client.recv(1024)
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
        client.send(message)
    
    

while True:
    client, address = serverSocket.accept()
    
    print(f'{str(address)} has enter the chat room!')
    
    # Make sure to change checking on the client side
    # Same with this one
    client.send('connection successful'.encode('ascii'))
    username = client.recv(1024)
    usernames.append(username)
    listOfClients.append(client)
    
    broadcast(f'{username} has enter the chat room!'.encode('ascii'))
    client.send('You are connected to the server!'.encode('ascii'))
    print(username, "is", f'{str(address)}')
    
    threading._start_new_thread(clientThread, (client,))