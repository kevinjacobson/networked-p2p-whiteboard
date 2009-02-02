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
        if len(self.recent_pos):
            delta = set()
            last_pos = self.recent_pos[0]
            for pos in self.recent_pos[1:]:
                if pos!=last_pos:
                    delta.add(Move((last_pos,pos),self.ownerid))
                last_pos = pos
            self.recent_pos = []
            print delta
            return delta

class Peers(btpeer.BTPeer,threading.Thread):
    
    def __init__( self, maxpeers, serverport, myid=None, serverhost = None ):
        btpeer.BTPeer.__init__(self, maxpeers, serverport, myid, serverhost)
        threading.Thread.__init__(self)
        self.debug = False
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
            move = Move(    (   (int(coords[1]),int(coords[2]))   ,  (int(coords[3]),int(coords[4]))   ),int(coords[0]))
            self.delta_moves.append(move)
        #print self.delta_moves
    def getMoves(self):
        temp = []
        temp.extend(self.delta_moves)
        self.delta_moves = []
        return temp
    def relay(self):
        self.buildMessage(self.getMoves())
        self.send_message()
    def send_message(self):
        if len(self.msg)>200:
            for i in self.peers.keys():
                threading.Thread(target=self.sendtopeer, args=[i,'MOVE',self.msg]).start()
            self.msg=""
            self.msg_moves=set()
    def buildMessage(self,moves):
        if moves != None:
            msgs = set()
            for move in set(moves):
                msgs.add(str(move))
            for txt in msgs:
                self.msg+=txt+"\n"
