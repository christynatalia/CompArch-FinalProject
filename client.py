import socket 
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

IP = '127.0.0.1'
PORT = 3000
HEADER_LENGTH = 10

message = tkinter.Tk()
message.withdraw()
username = simpledialog.askstring("Username", "Enter your username", parent = message)
#username = input("Enter your username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

guiDone = False
running = True

def usernameClient():
    while running:
        try:
            try:
                messageHeader = client.recv(HEADER_LENGTH)
                if not len(messageHeader):
                    return False
                
                messageLength = int(messageHeader.decode('ascii').strip())
                message = client.recv(messageLength).decode('ascii')
                
            except:
                message=client.recv(1024).decode('ascii')
            if message == 'username?':
                client.send(username.encode('ascii'))
            else:
                if guiDone:
                    textBox.config(state='normal')
                    textBox.insert('end', message)
                    textBox.yview('end')
                    textBox.config(state='disabled')
                print(message)
        except ConnectionAbortedError:
            break
        except:
            print("Error!")
            client.close()
            break

def sendClient():
    while True:
        #msgUser = input()
        msgUser = inputArea.get('1.0', 'end')
        message = f'{username}: {msgUser}'
        message = message.encode('ascii')
        messageHeader = f'{len(message):<{10}}'.encode('ascii')
        #messageUser = message.split()
        if msgUser == '/close':
            client.send(msgUser.encode('ascii'))
            client.close()
            break   
        else:
            client.send(messageHeader + message)
            inputArea.delete('1.0', 'end')
        
def guiLoop():
    window = tkinter.Tk()
    window.configure(bg="white")

    chatLabel = tkinter.Label(window, text="Chat:", bg="white")
    chatLabel.pack(padx=20, pady=5)

    textBox = tkinter.scrolledtext.ScrolledText(window)
    textBox.pack(padx=20, pady=5)
    textBox.config(state='disabled')

    messageLabel = tkinter.Label(window, text="Message:", bg="white")
    messageLabel.pack(padx=20, pady=5)

    inputArea = tkinter.Text(window, height=3)
    inputArea.pack(padx=20, pady=5)

    sendButton = tkinter.Button(window, text="Send", command=sendClient)
    sendButton.pack(padx=20, pady=5)

    guiDone = True
    window.protocol("WM_DELETE_WINDOW", stop)
    window.mainloop()

def stop():
    running = False
    window.destroy()
    client.close()
    exit(0)




thread_user_client = threading.Thread(target=usernameClient)
thread_user_client.start()

thread_send_client = threading.Thread(target=sendClient)
thread_send_client.start()

thread_gui = threading.Thread(target=guiLoop)
thread_gui.start()




