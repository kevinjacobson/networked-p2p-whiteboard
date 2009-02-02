import threading
import random
import socket
import SocketServer
import sys
import btpeer
import boardlisteners

class Server:  
    def __init__(self,clients):
        self.peerlistener = boardlisteners.Peers(100,1337)
        i = 1
        for client in clients:
            self.peerlistener.addpeer(1, client, 1337)
            i+=1
        self.peerlistener.start()
    
    

    def update(self):
        network_input = self.peerlistener.getMoves()
        self.broadcast(network_input)
        
    def broadcast(self,moves):
        self.peerlistener.buildMessage(moves)
        self.peerlistener.send_message()
        
    def run(self):
        while 1:           
            self.update()   
            
if __name__ == "__main__":
    server = Server(sys.argv[1:])
    server.run()
