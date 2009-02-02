import pygame
import threading
import random
import socket
import SocketServer
import sys
import btpeer

class Move:
    def __init__(self,points,ownerid):
        self.points=points
        self.start = points[0]
        
        self.end = points[1]
        str(self.end)+'-'+str(self.start)
        self.ownerid = ownerid
    def __str__(self):
        result = str(self.ownerid)+" " + str(self.start[0]) + " " + str(self.start[1]) + " " + str(self.end[0]) + " " + str(self.end[1]) 
        #print result
        return result

class MouseListener(threading.Thread):
    
    def __init__(self,ownerid):
        self.ownerid = ownerid
        threading.Thread.__init__(self)
        self.recent_pos = []
    def run(self):  
            pygame.event.poll()
            if pygame.mouse.get_pressed()[0]:
                self.recent_pos.append(pygame.mouse.get_pos())
            else:
                self.recent_pos = []
    def getMoves(self):
        recent_pos = []
        for pos in self.recent_pos:
            recent_pos.append(pos)
        
        delta_moves = []
        if len(recent_pos) < 3:
            return
        else:
            for i in range(1,len(recent_pos)):
                if recent_pos[i-1] != recent_pos[i]:
                    delta_moves.append(Move((recent_pos[i-1],recent_pos[i]),self.ownerid))
            self.recent_pos = recent_pos[-2:]
        return delta_moves

class Peers(btpeer.BTPeer,threading.Thread):
    
    def __init__( self, maxpeers, serverport, myid=None, serverhost = None ):
        btpeer.BTPeer.__init__(self, maxpeers, serverport, myid, serverhost)
        threading.Thread.__init__(self)
        self.debug = True
        self.delta_moves = []
        self.addhandler('MOVE', self.movesHandler)
        self.msg_moves = set()
        self.msg = ""
        self.counter = 1
    def run(self):
        self.mainloop()
    def movesHandler(self,peercon,msg):
        #print "Message:\n"
        for line in msg.splitlines():
            coords = line.split(" ")
            move = Move(    (   (int(coords[1]),int(coords[2]))   ,  (int(coords[3]),int(coords[4]))   ),    int(coords[0]))
            self.delta_moves.append(move)
        #print self.delta_moves
                
    def getMoves(self):
        temp = []
        temp.extend(self.delta_moves)
        self.delta_moves = []
        return temp
    def send_message(self):
                if len(self.msg)>120:
                    for i in self.peers.keys():
                        print "SENDING TO PEER!"
                        print i
                        print self.msg
                        threading.Thread(target=self.sendtopeer, args=[i,'MOVE',self.msg]).start()
                    self.msg=""
                
    def buildMessage(self,moves):
        if moves != None:
            for move in moves:
                self.msg+=str(move)+"\n"
