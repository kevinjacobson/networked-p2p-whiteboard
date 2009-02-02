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
            
COLORS = [(255,0,0),(0,255,0),(255,255,0),(0,255,255)]        


class App:  
    def __init__(self,is_client=True):
        self.is_client = is_client
                              #Initialize the pygame modules
        self.background_color = 0,0,0
        self.width,self.height = self.size = DEFAULT_SIZE     #Set the screen dimensions
        if is_client:
            pygame.init()    
            self.screen = pygame.display.set_mode(self.size)  #Grab the display surface
            self.board = Board(self.size)                     #Create a new surface to draw onto
            self.mouselistener = boardlisteners.MouseListener(0)   
        self.peerlistener = boardlisteners.Peers(100,1337)
        self.add_peers(sys.argv[1:])
        self.peerlistener.start()
    
    def add_peers(self,connecting_peers):
        i = 1
        for peer in connecting_peers:
            self.peerlistener.addpeer(i,peer,1337)
            i+=1
    

    def update(self):
        network_input = self.peerlistener.getMoves()
        if self.is_client:
            pygame.event.poll()
            self.screen.fill(self.background_color)
            self.mouselistener.run()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.board.clear()      #Have this also send a message
            local_input = self.mouselistener.getMoves()
            self.draw(network_input)
            self.draw(local_input)
            self.broadcast(local_input)
        else:
            self.broadcast(network_input)
        
    def draw(self,moves):
        self.board.draw_moves(moves)
        self.screen.blit(self.board.surface,pygame.Rect((0,0),self.size))
        pygame.display.flip()
    
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
    app = App()
    app.add_peers(["129.21.20.153"])
    app.run()
