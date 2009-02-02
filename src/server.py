#!/usr/bin/python
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
            self.peerlistener.addpeer(i, client, 1337)
            i+=1
        self.peerlistener.start()
    
    def update(self):
        while 1:           
            self.peerlistener.relay()   
            
if __name__ == "__main__":
    print sys.argv[1:]
    server = Server(sys.argv[1:])
    server.update()
