import random

#Values for Orange PNG start at 240
#Values for player start at 230ish

class User:
    def __init__(self, pos, char, diff=-1):
        self.x = pos[0]
        self.y = pos[1]
        self.path = []
        self.char = char
        self.prev_char = None
        self.prev_move = None
        self.old = None
        self.diff = diff
    
        self.CHAR_START = 240 #USER char repr
        if diff == -1:
            self.CHAR_START = 228 #CORRUPTION char repr
    
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
    
    def derezzed(self):
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
#Node is the map at a given point in time

class Computer(User):
    def make_move(self, MAP, MAP_WIDTH, MAP_HEIGHT):
        if self.diff == 0:
            self.random(MAP, MAP_WIDTH, MAP_HEIGHT)
        elif self.diff == 1:
            print "TODO"
        elif self.diff == 2:
            print "TODO"

    def random(self, MAP, MAP_WIDTH, MAP_HEIGHT):
        x = random.randint(0, 4)
        if x == 0:
            self.move("NORTH")
        elif x == 1:
            self.move("SOUTH")
        elif x == 2:
            self.move("WEST")
        elif x == 3:
            self.move("EAST")

        
