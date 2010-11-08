#! /usr/bin/env python
"""
Solves the voronoi problem
"""

import sys
import os
import time

start_time = time.time()
num_turns = None
num_players = None
my_num = None
turn = None
board = None

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

class MySocket:
# from http://docs.python.org/howto/sockets.html
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        sent = self.sock.send(msg + "\n")
        if sent == 0:
            raise RuntimeError("socket connection broken")
        
    def myrecv(self):
        while 1:
            data = self.sock.recv(1024)
            if not data or data == "Bye" or "\n" in data: break
        print 'Received',repr(data)
        return data

    def close(self):
        if self.sock is None:
            pass
        else:
            self.sock.close()

class GameState:
    def __init__(self):
        self.state = []
        for i in range(400):
            self.state.append([])
            for j in range(400):
                self.state[i].append([])

        
    def update_board(self,x,y,p):
        self.state[x][y] = p

    def score_board(self):
        
        return score

def parse_data(data):
    data = data.split(' ')
    if (len(data) == 4) and (num_turns is None):
        num_turns,num_players,my_num,turn = data
    if "YOURTURN" in data:
        send = make_move()
    elsif (len(data) == 3):
        x_move,y_move,player = data
        update_board(x_move,y_move,player)

def make_move():
    pass

def update_board():
    pass

if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    for line in sys.stdin:
        
    s = MySocket()
    s.connect("localhost", 44444)
    s.mysend(tag)
    data = ""
    while ['WIN','LOSE'] not in data:
        data = s.myrecv()
        if data:
            m = parse_data(data):
            if len(m) > 0:
                s.mysend(m)
    s.close()

    print "Time: ",round(time.time() - start_time)
    
