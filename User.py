class User:
    def __init__(self, pos, char):
        self.x = pos[0]
        self.y = pos[1]
        self.path = []
        self.char = char
        self.prev_char =None
        self.old = None
    
    def __str__(self):
        return self.char

    def move(self, direct):
        self.old = (self.x, self.y)
        if direct == "NORTH":
            self.prev_char = '|'
            self.y -= 1
        elif direct == "SOUTH":
            self.prev_char = '|'
            self.y += 1
        elif direct == "WEST":
            self.prev_char = '-'
            self.x -= 1
        elif direct == "EAST":
            self.prev_char = '-'
            self.x += 1
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False

    
