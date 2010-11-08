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
from PIL import Image
imgx = 400
imgy = 400
image = Image.new("RGB", (imgx, imgy))

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
    def __init__(self, moves = []):
        self.moves = moves
        self.scores = [-1]*num_turns*2
        self.score = 0
        self.state = []
        self.p0score = -1
        self.p1score = -1
        for i in range(board_size):
            self.state.append([])
            for j in range(board_size):
                self.state[i].append([])
        
    def make_move(self,x,y):
        x = int(x)
        y = int(y)
        if len(self.moves) > 0:
            self.moves.append([x,y])
        else:
            self.moves = [[x,y]]

    def score_board(self):
        nx = []
        ny = []
        if len(self.moves) > 2:
            for move in self.moves:
                nx.append(move[0])
                ny.append(move[1])
        elif len(self.moves) == 2:
            nx = self.moves[0]
            ny = self.moves[1]

        if len(self.moves) <= 2:
            self.p0score = board_size ** 2
            self.p1score = 0

        else:
            for y in range(board_size):
                for x in range(board_size):
                    # find the closest move
                    dmin = math.hypot(board_size - 1, board_size - 1)
                    j = -1
                    for i in range(num_turns*2):
                        try:
                            d = math.hypot(nx[i] - x, ny[i] - y)
                            if d < dmin:
                                dmin = d
                                j = i
                                p = i % 2
                        except:
                            # out of range
                            pass
                    if j > -1:
                        self.state[x][y] = p
                        self.scores[j] += 1

            self.p0score = 0
            self.p1score = 0

            for y in range(board_size):
                for x in range(board_size):
                    if self.state[x][y] == 0:
                        self.p0score += 1
                    else:
                        self.p1score += 1

        return self.p0score, self.p1score

def generate_move(board):
    # Generate a random move		
    st = time.time()
    max_score = 0
    orig_moves = board.moves + []
    print "Orig moves",orig_moves
    best_move = [0,0]
    while(time.time() - st < (120 / num_moves - 1)):
        x = random.randint (0, board_size)
        y = random.randint (0, board_size)

        # If it's been done, generate until
        # we get a fresh one.
        while [x,y] in board.moves:
                x = random.randint (0, board_size)
                y = random.randint (0, board_size)

        new_moves = orig_moves + [[x,y]]
        if len(new_moves) == 1:
            print "First move!"
            return 200,200 # hard code the first move!
        print "New moves",new_moves
        g = GameState(moves=new_moves)
        g.score_board()
        print x, y
        print g.p0score
        if g.p0score > max_score:
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
            x,y = generate_move(board)

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
