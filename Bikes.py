import random

#Values for Orange PNG start at 240
#Values for player start at 230ish
from CYLGame import Player


class Bike(Player):
    def __init__(self, pos, char, prog):
        super(Bike, self).__init__(prog)
        self.x = pos[0]
        self.y = pos[1]
        self.path = []
        self.char = char
        self.prev_char = None
        self.prev_move = None
        self.old = None
        self.derezzed = False

        self.CHAR_START = 228

    def __str__(self):
        return self.char

    def pos(self):
        return (self.x, self.y)

    def move(self, direct):
        self.old = (self.x, self.y)
        self.path += [self.old]
        if direct == "NORTH":
            self.y -= 1
        elif direct == "SOUTH":
            self.y += 1
        elif direct == "WEST":
            self.x -= 1
        elif direct == "EAST":
            self.x += 1
        self.det_prev_char(direct)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False

    def derezz(self):
        return self.path
#I will need to implement an algorithm for the corruption to utilize when making their decisions.
#A suggested implementation is to use a minimax algorithm. https://www.sifflez.org/misc/tronbot/
    def det_prev_char(self, move):
        if self.prev_move == None:
            if move == "NORTH" or move == "SOUTH":
                self.prev_char = chr(self.CHAR_START)
            else:
                self.prev_char = chr(self.CHAR_START + 1)
        else:
            index = 0
            if self.prev_move == "EAST":
                if move == "NORTH":
                    index = 2
                elif move == "SOUTH":
                    index = 5
                else:
                    index = 1
            elif self.prev_move == "WEST":
                if move == "NORTH":
                    index = 3
                elif move == "SOUTH":
                    index = 4
                else:
                    index = 1
            elif self.prev_move == "NORTH":
                if move == "WEST":
                    index = 5
                elif move == "EAST":
                    index = 4
                else:
                    index = 0
            elif self.prev_move == "SOUTH":
                if move == "WEST":
                    index = 2
                elif move == "EAST":
                    index = 3
                else:
                    index = 0
            self.prev_char = chr(self.CHAR_START + index)
        self.prev_move = move

    def handle_move(self, state):
        move = state["move"]

        if move == "w":
            self.move("NORTH")
        if move == "s":
            self.move("SOUTH")
        if move == "a":
            self.move("WEST")
        if move == "d":
            self.move("EAST")
        if move == "Q":
            self.derezzed = True
