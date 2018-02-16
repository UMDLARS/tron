import random

#Values for Orange PNG start at 240
#Values for player start at 230ish
from CYLGame import Player
from CYLGame.Player import DefaultGridPlayer, Prog


class Bike(DefaultGridPlayer):
    ILLEGAL_CHARS = ["|", "=", "-"]
    NUM_OF_SENSORS = 8

    def __init__(self, pos, char, prog, bot_consts):
        super(Bike, self).__init__(prog, bot_consts)
        self.x = pos[0]
        self.y = pos[1]
        self.path = []
        self.char = char
        self.prev_char = None
        self.prev_move = None
        self.old = None
        self.derezzed = False
        self.sensor_coords = []

        self.CHAR_START = 228

    def __str__(self):
        return self.char

    def pos(self):
        return (self.x, self.y)

    def do_move(self, direct):
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

    def update_state(self, state):
        super(Bike, self).update_state(state)
        # move = chr(state.get("move", ord("Q")))

        if self.move == "w":
            self.do_move("NORTH")
        if self.move == "s":
            self.do_move("SOUTH")
        if self.move == "a":
            self.do_move("WEST")
        if self.move == "d":
            self.do_move("EAST")
        if self.move == "Q":  # Should this be an else statement. Then any invalid input is the same as quiting.
            self.derezzed = True

        self.update_sensors(state)

    def update_sensors(self, state):
        self.sensor_coords = []
        for i in range(self.NUM_OF_SENSORS):
            x_name = "s" + str(i + 1) + "x"
            y_name = "s" + str(i + 1) + "y"
            self.sensor_coords.append((state.get(x_name, "0"), state.get(y_name, "0")))


class DumbComputer(Prog):
    def __init__(self):
        super(DumbComputer, self).__init__()
        self.last_move = None

    def run(self, state=None, max_op_count=-1, random=None):
        if random is None:
            import random
        moves = list(map(ord, ["w", "a", "s", "d"]))

        if self.last_move:
            if self.last_move == ord("w"):
                moves.remove(ord("s"))
            if self.last_move == ord("s"):
                moves.remove(ord("w"))
            if self.last_move == ord("a"):
                moves.remove(ord("d"))
            if self.last_move == ord("d"):
                moves.remove(ord("a"))
            self.last_move = random.choice(moves)
            return {"move": self.last_move}
        else:
            self.last_move = random.choice(moves)
            return {"move": self.last_move}
