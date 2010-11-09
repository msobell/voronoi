#! /usr/bin/env python
"""
Solves the voronoi problem
"""

import socket
import string
import random
import math
import sys
import os
import time

HOST = '127.0.0.1'
PORT = 20000

start_time = time.time()
num_turns = None
num_players = None
my_num = None
board_size = None
turn = None
board = None

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

class GameState:
    def __init__(self, moves = [[]], moves_done = 0):
        self.moves = moves
        self.score = 0
        self.state = []
        self.p0score = -1
        self.p1score = -1
        self.moves_done = moves_done
        for i in range(board_size):
            self.state.append([])
            for j in range(board_size):
                self.state[i].append([])
        
    def make_move(self,x,y):
        x = int(x)
        y = int(y)
        if self.moves_done == 0:
            self.moves = [[x,y]]
        else:
            self.moves.append([x,y])
        self.moves_done += 1

    def score_board(self):
        nx = []
        ny = []
        print "Self.moves",self.moves
        if self.moves_done > 0:
            for move in self.moves:
                nx.append(move[0])
                ny.append(move[1])

            print "nx:",nx
            print "ny:",ny
            for y in range(board_size):
                for x in range(board_size):
                    # find the closest move
                    dmin = math.hypot(board_size - 1, board_size - 1)
                    j = -1
                    for i in range(self.moves_done):
                        d = math.hypot(nx[i] - x, ny[i] - y)
                        if d < dmin:
                            dmin = d
                            j = i
                            p = i % 2
                    if j > -1:
                        self.state[x][y] = p

            self.p0score = 0
            self.p1score = 0

            for y in range(board_size):
                for x in range(board_size):
                    if self.state[x][y] == 0:
                        self.p0score += 1
                    else:
                        self.p1score += 1
        else:
            print "Num moves:",self.moves_done
            self.p0score = board_size ** 2
            self.p1score = 0

        return self.p0score, self.p1score

def generate_move(board):
    max_score = 0
    orig_moves = board.moves + []
    print "Orig moves",orig_moves
    mcount = 0
    tries = []
    for move in board.moves:
        if my_num == 1:
            mn = 1
        else:
            mn = 0
        if mcount % 2 == mn:
            tries.append([move[0]+1,move[1]+1])
            tries.append([move[0]-1,move[1]-1])
        mcount += 1
        
    if len(tries) == 0:
        tries = [[200,200]]
    
    best_move = None

    print "Tries:",tries
    print "Moves:",board.moves

    for t in tries:
        print "Try:",t
        # Don't take up more than your fair share of time
        # if (time.time() - start_time) < (120 / (num_turns - board.moves_done)) and t not in board.moves:
        if t not in board.moves:
            x = t[0]
            y = t[1]
            new_moves = orig_moves + [[x,y]]
            if board.moves_done == 0:
                print "First move!"
                return 200,200 # hard code the first move!
            print "New moves",new_moves
            g = GameState(moves=new_moves,moves_done=board.moves_done)
            g.score_board()
            print x,y
            tscore = 0
            if my_num == 1:
                tscore = g.p0score
                print g.p0score
            else:
                tscore = g.p1score
                print g.p1score
            if tscore > max_score:
                max_score = tscore
                best_move = [[x,y]]
            
    return best_move[0][0], best_move[0][1]

## From:
## Charles J. Scheffold
## cjs285@nyu.edu
def SReadLine (conn):
    data = ""
    while True:
        c = conn.recv(1)
        if not c:
            time.sleep (1)
            break
        data = data + c
        if c == "\n":
            break
    return data

if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    # Open connection to voronoi server
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))

    print "Connected to", HOST, "port", PORT

    # Read status line
    data = SReadLine (s)
    line = string.strip (data)

    # Split status fields into a list
    status = string.split (line)

    print "BoardSize:", status[0]
    print "NumTurns:", status[1]
    print "NumPlayers:", status[2]
    print "MyPlayerNumber:", status[3]
    print ""

    # Save the board size for later
    board_size = int (status[0])
    num_turns = int (status[1])
    num_players = int (status[2])
    my_num = int (status[3])

    board = GameState()

    while True:
        # Read one line from server
        data = SReadLine (s)

        p1score,p2score = board.score_board()
        print p1score, p2score, p1score+p2score

        # If it's empty, we are finished here
        if data == None or data == '':
            break

        # Strip the newline
        line = string.strip (data)

        # Receive YOURTURN
        if (line == "YOURTURN"):		
            print
            print line

            # Generate a move here
            try:
                x,y = generate_move(board)
            except:
                x = 74
                y = 89

            # Save move for duplicate checking
            board.make_move(x,y)

            print "MY MOVE:", (x,y)

            # Wait a little (so we can watch the game at a decent speed)
            # and then send the move
            # time.sleep (.5)
            s.send ("%d %d\n" % (x,y))

        # Receive WIN
        elif (line == "WIN"):
            print ("I WIN!")
            break

        # Receive LOSE
        elif (line == "LOSE"):
            print ("I LOSE :(")
            break

        # Receive an opponent's move data
        else:
            move = string.split (line)
            board.make_move(move[0], move[1])
            print "OPPONENT MOVE:", move
    # Poof!
    s.close ()

    print time.time() - start_time
