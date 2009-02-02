import pygame
import threading
import random
import socket
import SocketServer
import sys
import btpeer
import boardlisteners

DEFAULT_SIZE = 800,600

class Board:

    def __init__(self,size,background_color=(255,255,255)):
        self.size = self.x, self.y = size
        self.surface = pygame.Surface(self.size) 
        self.background_color = background_color
        self.clear()
    def clear(self):
        self.surface.fill(self.background_color)
        
    def draw_moves(self,moves):
        if moves != None:
            for move in moves:
                print move
                pygame.draw.aaline(self.surface,COLORS[move.ownerid],move.points[0],move.points[1],10)
             


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
    server = Server(["localhost"])
    server.run()
