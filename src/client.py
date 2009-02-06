#!/usr/bin/python
import pygame
import threading
import random
import socket
import SocketServer
import sys
import btpeer
import boardlisteners
import random
 
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
                pygame.draw.aaline(self.surface,COLORS[move.ownerid],move.points[0],move.points[1],10)
            
COLORS = [(255,0,0),(0,255,0),(255,0,255),(0,255,255),(0,0,0)]        


class App:  
    def __init__(self,*address):
        self.count=1
        self.background_color = 0,0,0
        self.width,self.height = self.size = DEFAULT_SIZE     #Set the screen dimensions
        pygame.init()    
        self.screen = pygame.display.set_mode(self.size)  #Grab the display surface
        self.board = Board(self.size)                     #Create a new surface to draw onto
        self.mouselistener = boardlisteners.MouseListener(random.randint(0,4))   
        self.peerlistener = boardlisteners.Peers(100,1337)
        index = 1
        for peer in address:
            self.peerlistener.addpeer(index,peer,1337)
            index+=1
        self.peerlistener.start()
        self.output = set() 

    def update(self):
        network_input = self.peerlistener.getMoves()
        pygame.event.poll()
        self.screen.fill(self.background_color)
        if self.count%5==0: #Prevents too much data from being collected
            self.mouselistener.run()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.board.clear()      #Have this also send a message
        new_moves = self.mouselistener.getMoves()
        local_input = list()
        if new_moves:
            for move in new_moves:
                self.output.add(move)
            local_input = list(set(self.output))
        self.draw(network_input)
        #self.draw(local_input)
        self.broadcast(local_input)
        self.output=set()
        self.count+=1
        pygame.display.flip()

    def draw(self,moves):
        self.board.draw_moves(moves)
        self.screen.blit(self.board.surface,pygame.Rect((0,0),self.size))
        
    
    def broadcast(self,moves):
        self.peerlistener.buildMessage(moves)
        self.peerlistener.send_message()
        
    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() 
            self.update()   
            
if __name__ == "__main__":
    app = App(sys.argv[1])
    app.run()
