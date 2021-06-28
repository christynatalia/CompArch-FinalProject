import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

IP = '127.0.0.1'
PORT = 3000

class Client:
    
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip,port))
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        self.username = simpledialog.askstring("Username", "Enter your username", parent = msg)
        
        self.guiDone = False
        
        self.running = True
        
        guiThread = threading.Thread(target= self.guiLoop)
        receiveThread = threading.Thread(target = self.receiveClient)
        
        guiThread.start()
        receiveThread.start()
        
        
    def guiLoop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="black")
        
        self.chatLabel = tkinter.Label(self.window, text = "Chat", bg="black", fg="white")
        self.chatLabel.config(font=("Dubai Medium", 16))
        self.chatLabel.pack(padx=20, pady=5)
        
        self.textArea = tkinter.scrolledtext.ScrolledText(self.window)
        self.textArea.pack(padx = 20, pady=5)
        self.textArea.config(state='disabled')
        
        self.msgLabel = tkinter.Label(self.window, text = "Message", bg="black", fg="white")
        self.msgLabel.config(font=("Dubai Medium", 16))
        self.msgLabel.pack(padx=20, pady=5)
        
        self.inputArea = tkinter.Text(self.window, height=3)
        self.inputArea.pack(padx=20, pady=5)
        
        self.sendButton = tkinter.Button(self.window, text='Send', command=self.sendClient)
        self.sendButton.config(font=("Dubai Medium", 14))
        self.sendButton.pack(padx=20, pady=5)
        
        
        self.guiDone = True
        
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()


    def sendClient(self):
        msgUser = self.inputArea.get('1.0', 'end')
        
        message = f"{self.username}:{msgUser}"
        message = message.encode('ascii')
        
        messageHeader = f'{len(message):<{10}}'.encode('ascii')
        
        if '/close' in msgUser:
            self.client.send(self.inputArea.get('1.0', 'end').encode('ascii'))
            self.window.destroy()
            self.window.mainloop()

        else:
            self.client.send(messageHeader + message)
        
        self.inputArea.delete('1.0', 'end')
        
        
    def stop(self):
        self.running = False
        self.window.destroy()
        self.client.close()
        exit(0)
      
        
    def receiveClient(self):
        while self.running:
            try:
                try:
                    messageHeader = self.client.recv(10)
                    if not len(messageHeader):
                        return False
                    
                    messageLength = int(messageHeader.decode('ascii').strip())
                    message = self.client.recv(messageLength).decode('ascii')
                    
                    
                except:
                    message = self.client.recv(1024).decode('ascii')
                    
                
                if message == 'username?':
                    self.client.send(self.username.encode('ascii'))
                
                else:
                    if self.guiDone:
                        self.textArea.config(state="normal")
                        self.textArea.insert('end', message)
                        self.textArea.yview('end')
                        self.textArea.config(state='disabled')

            
            except:
                self.client.close()
                break
                
    
    
client = Client(IP, PORT)