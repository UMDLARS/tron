import random

#Values for Orange PNG start at 240
#Values for player start at 230ish

class User:
    ILLEGAL_CHARS = ["|", "=", "-"]
    def __init__(self, pos, char):
        self.x = pos[0]
        self.y = pos[1]
        self.path = []
        self.char = char
        self.prev_char = None
        self.prev_move = None
        self.old = None
    
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
#Node is the map at a given point in time

class Computer(User):
    def __init__(self, pos, char, diff):
        User.__init__(self, pos, char)
        self.diff = diff
        self.CHAR_START = 240 #USER char repr
        self.derezzed = False

    def make_move(self, MAP, MAP_WIDTH, MAP_HEIGHT):
        if self.diff == 0:
            self.random(MAP, MAP_WIDTH, MAP_HEIGHT)
        elif self.diff == 1:
            move = self.better_move(MAP, MAP_WIDTH, MAP_HEIGHT)
            self.move(move)
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


    def get_neighbors(self, m, w, h, pos):
        nbors = []
        x = pos[0]
        y = pos[1]
        if x - 1 >= 0 :
            nbors += [(x-1, y)]
        if x + 1 < h:
            nbors += [(x+1, y)]
        if y - 1 >= 0:
            nbors += [(x, y-1)]
        if y + 1 < h:
            nbors += [(x, y+1)]
        return nbors
    
    def better_move(self, tronmap, width, height):
        visited = self.build_map(tronmap, width, height)
        pos = [] #Most advantageous move
        if  self.y - 1 >= 0 and tronmap[(self.x, self.y-1)] == ' ':
            pos += [("NORTH", self.bfs(visited, width, height, self.x, self.y-1))]  
        if self.y + 1 < height and tronmap[(self.x, self.y+1)] == ' ':
            pos += [("SOUTH", self.bfs(visited, width, height, self.x, self.y+1))]  
        if self.x - 1 >= 0 and tronmap[(self.x-1, self.y)] == ' ':
            pos += [("WEST", self.bfs(visited, width, height, self.x-1, self.y))]  
        if self.x + 1 < width and tronmap[(self.x+1, self.y)] == ' ':
            pos += [("EAST", self.bfs(visited, width, height, self.x+1, self.y))]
        
        if not pos:
            return "NORTH" #Gonna die, just pick a direction
        return max(pos, key=lambda i:i[1])[0]

    def build_map(self, tronmap, width, height):
        visited = {}
        for i in range(0, height):
            for j in range(0, width):
                if tronmap[(j,i)] == ' ': 
                    visited[(j,i)] = False 
                else:
                    visited[(j,i)] = True
        return visited

    def print_map(self, m, w, h):
        for i in range(0, h):
            for j in range(0, w):
                if visited[(j,i)] == True:
                    print "X",
                else:
                    print ' ',
            print "/"

    #Gonna use this to evaluate how strong of a position we are in. This will count the open amount of spaces we have which we will use to evaluate which direction the bike should go
    def bfs(self, m, w, h, x, y):
        queue = []
        visited = []
        path = {} #Not gonna bother with path. 
        start = (x,y)
        path[start] = (None, None)
        queue += [start]

        while queue:
            cur = queue.pop()

            for i in self.get_neighbors(m, w, h, cur):
                if not m[i] and i not in visited:
                    queue += [i]

            visited += [cur]

        return len(visited)
