import socket
import threading
import os 
import time

##base code imported from https://github.com/sheriffolaoye/same-network-group-chat/tree/chat-app-tutorial

clients = {}
last_message = {}

admins = open('admin.txt','a+')
admins.truncate(0)

f = open('users.txt','a+')
f.truncate(0)

class Server(object):
    def __init__(self, hostname, port):
        
        #list where clients are stored

        # create server socket
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # start server
        self.tcp_server.bind((hostname, port))
        self.tcp_server.listen(5)

        print("[INFO] Server running on {}:{}".format(hostname, port))
            
        # Accept new users.
        while True:
            connection, address = self.tcp_server.accept()
            nickname = connection.recv(1024)
            nickname = nickname.decode('utf-8')
            f = open('users.txt','a+')
            filesize = os.path.getsize("users.txt")
            
            f.write(nickname)
            f.write("\n")
            f.close()
            
            if filesize == 0 :
                admin = open('admin.txt','a+')
                admin.write(nickname)
                admin.close()
                
                
            clients[nickname] = connection
            
            # start a thread for the client
            threading.Thread(target=self.receive_message, args=(connection, nickname), daemon=True).start()
            

            print("[INFO] Connection from {}:{} AKA {}".format(address[0], address[1], nickname))
            
            sender = "server"
            message = ("user " + nickname + " has " + "connected")
            message = message.encode('utf-8')
            self.send_message(message,sender)
    
    def receive_message(self, connection, nickname):
        print("[INFO] Waiting for messages")
        while True:            
    
            try:
                message = connection.recv(1024)
                msg = message.decode('utf-8')
                
                if msg.startswith('kick'):
                    message = msg.split(" ")
                    name_to_kick = message[2]
                    print(message[2])
                    
                    self.kick_user(name_to_kick)
                    
                else:
                    self.send_message(message, nickname)
                    print(nickname + ": " + message.decode('utf-8'))
            except:
                if nickname in clients:    
                    connection.close()
                    del(clients[nickname])
                admins = open('admin.txt','r+')
                admin = admins.read()
                if nickname == admin :
                    sender = "server"
                    message = ("admin " + nickname + " has " + "disconnected")
                    message = message.encode('utf-8')
                    self.send_message(message,sender)
                 
                    admins.truncate(0)
                    with open("users.txt","r+") as f:
                        lines = f.readlines()
                    admins.seek(0)
                    admins.write(lines[1])
                    message = ("New admin: " + lines[1])
                    message = message.encode('utf-8')
                    self.send_message(message,sender)
                    admins.close()
                sender = "server"
                message = ("user " + nickname + " has " + "disconnected")
                message = message.encode('utf-8')
                self.send_message(message,sender)
                with open("users.txt","r+") as f:
                    f.truncate(0)
                    for nickname in clients:
                        f.write(nickname)
                        f.write("\n")
                break

                


    def send_message(self, message, sender):
        if len(clients) > 0:
            for nickname in clients:
                if nickname != sender:
                    msg = sender + ": " + message.decode('utf-8')
                    clients[nickname].send(msg.encode('utf-8'))
      
         
    #kicking users    
    def kick_user(self,nickname):
        if nickname in clients:
            clients[nickname].send('You were kicked by admin'.encode('utf-8'))
            clients[nickname].send('Closing the chat'.encode('utf-8'))
            clients[nickname].close()
            del(clients[nickname])
        
            
        
if __name__ == "__main__":
    port = 5555
    hostname = "localhost"

    chat_server = Server(hostname, port)