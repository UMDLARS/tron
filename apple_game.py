from __future__ import print_function
import sys
import math
import random
from collections import defaultdict
from CYLGameServer import serve
from CYLGameServer import CYLGameLanguage
from CYLGameServer import CYLGame


# WARNING: this does not do bounds checking
class Map(object):
    def __init__(self, default_char=''):
        self.char_to_ps = defaultdict(set)
        self.p_to_char = defaultdict(lambda: default_char)
        self.default_char = default_char
        self.changes = {}

    def __setitem__(self, key, value):
        self.add(value, key)

    def __getitem__(self, item):
        return self.get_char_at(item)

    # changes in the format of a dictionary
    # key: (x, y)
    # value: new_char
    def get_diff(self):
        changes = self.changes
        self.changes = {}
        return changes

    # pos must be tuple
    def add(self, char, pos):
        assert type(pos) == tuple
        if pos in self.p_to_char.keys():
            self.rm_char(pos)
        self.char_to_ps[char].add(pos)
        self.p_to_char[pos] = char
        self.changes[pos] = char

    # pos must be tuple
    def rm_char(self, pos):
        assert type(pos) == tuple
        char = self.p_to_char[pos]
        del self.p_to_char[pos]
        if char in self.char_to_ps and pos in self.char_to_ps[char]:
            self.char_to_ps[char].remove(pos)
            self.changes[pos] = self.default_char

    # returns a set of pos
    def get_all_pos(self, char):
        return self.char_to_ps[char]

    # will return default_char if the position is not set
    def get_char_at(self, pos):
        return self.p_to_char[pos]


class AppleFinder(CYLGame):
    MAP_WIDTH = 80
    MAP_HEIGHT = 25
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = MAP_HEIGHT + 6
    MSG_START = 20
    MAX_MSG_LEN = SCREEN_WIDTH - MSG_START - 1
    CHAR_WIDTH = 8
    CHAR_HEIGHT = 8
    GAME_TITLE = "Apple Hunt"

    APPLE_EATING_RESPONSES = ["Yummy!", "That hit the spot!", "Wow!", "Amazing!", "So good!",
                              "An apple a day keeps the robots away.", "Yummy in the tummy!", "Oh my, that was good!",
                              "Bon appetit", "Ewwww, I think that one had a worm."]

    NUM_OF_APPLES = 4
    NUM_OF_PITS_START = 0
    NUM_OF_PITS_PER_LEVEL = 8
    MAX_TURNS = 200

    PLAYER = '@'
    APPLE = 'O'
    EMPTY = ' '
    PIT = '^'

    def __init__(self):
        self.running = True
        self.in_pit = False
        centerx = self.MAP_WIDTH / 2
        centery = self.MAP_HEIGHT / 2
        self.player_pos = [centerx, centery]
        self.apples_eaten = 0
        self.apples_left = 0
        self.apple_pos = []
        self.objects = []
        self.turns = 0
        self.level = 0
        self.msgs = ["Welcome to "+self.GAME_TITLE+"!!!", "Try to eat as many apples as possible"]

        self.__create_map()

    def __create_map(self):
        # self.map = [[self.EMPTY] * self.MAP_WIDTH for _ in range(self.MAP_HEIGHT)]
        self.map = Map(self.EMPTY)

        self.map[(self.player_pos[0], self.player_pos[1])] = self.PLAYER

        self.place_apples(self.NUM_OF_APPLES)
        self.place_pits(self.NUM_OF_PITS_START)

    def place_apples(self, count):
        self.place_objects(self.APPLE, count)
        self.apples_left = self.apples_left + count

    def place_pits(self, count):
        self.place_objects(self.PIT, count)

    def place_objects(self, char, count):
        placed_objects = 0
        while placed_objects < count:
            x = random.randint(0, self.MAP_WIDTH - 1)
            y = random.randint(0, self.MAP_HEIGHT - 1)

            if self.map[(x, y)] == self.EMPTY:
                self.map[(x, y)] = char
                placed_objects += 1

    def handle_key(self, key):
        self.turns += 1

        self.map[(self.player_pos[0], self.player_pos[1])] = self.EMPTY
        if key == "w":
            self.player_pos[1] -= 1
        if key == "s":
            self.player_pos[1] += 1
        if key == "a":
            self.player_pos[0] -= 1
        if key == "d":
            self.player_pos[0] += 1
        if key == "Q":
            self.running = False
            return

        self.player_pos[0] %= self.MAP_WIDTH
        self.player_pos[1] %= self.MAP_HEIGHT
        if self.map[(self.player_pos[0], self.player_pos[1])] == self.APPLE:
            self.apples_eaten += 1
            self.apples_left -= 1
            self.msgs += [random.choice(list(set(self.APPLE_EATING_RESPONSES)-set(self.msgs[-3:])))]
        elif self.map[(self.player_pos[0], self.player_pos[1])] == self.PIT:
            self.in_pit = True
        self.map[(self.player_pos[0], self.player_pos[1])] = self.PLAYER

        if self.apples_left == 0:
            self.level += 1
            self.place_apples(self.NUM_OF_APPLES)
            self.place_pits(self.NUM_OF_PITS_PER_LEVEL)

    def is_running(self):
        return self.running

    def find_closest_apple(self, x, y):
        apple_pos_dist = []
        for pos in self.map.get_all_pos(self.APPLE):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    a_x, a_y = pos[0]+(self.SCREEN_WIDTH*i), pos[1]+(self.SCREEN_HEIGHT*j)
                    dist = math.sqrt((a_x-x)**2 + (a_y-y)**2)
                    direction = [a_x-x, a_y-y]
                    if direction[0] > 0:
                        direction[0] = 1
                    elif direction[0] < 0:
                        direction[0] = -1
                    if direction[1] > 0:
                        direction[1] = 1
                    elif direction[1] < 0:
                        direction[1] = -1
                    # Make them ones.
                    apple_pos_dist += [(dist, direction)]

        apple_pos_dist.sort()
        if len(apple_pos_dist) > 0:
            return apple_pos_dist[0][1]
        else:
            raise Exception("We didn't find an apple")

    def get_vars_for_bot(self):
        bot_vars = {}

        # get closest apple
        spots = []
        # while spots
        x_dir, y_dir = self.find_closest_apple(*self.player_pos)

        x_dir_to_char = {-1: ord("a"), 1: ord("d"), 0: 0}
        y_dir_to_char = {-1: ord("w"), 1: ord("s"), 0: 0}

        bot_vars = {"x_dir": x_dir_to_char[x_dir], "y_dir": y_dir_to_char[y_dir],
                    "pit_to_east": 0, "pit_to_west": 0, "pit_to_north": 0, "pit_to_south": 0}

        if self.map[((self.player_pos[0]+1)%self.SCREEN_WIDTH, self.player_pos[1])] == self.PIT:
            bot_vars["pit_to_east"] = 1
        if self.map[((self.player_pos[0]-1)%self.SCREEN_WIDTH, self.player_pos[1])] == self.PIT:
            bot_vars["pit_to_west"] = 1
        if self.map[(self.player_pos[0], (self.player_pos[1]-1)%self.SCREEN_HEIGHT)] == self.PIT:
            bot_vars["pit_to_north"] = 1
        if self.map[(self.player_pos[0], (self.player_pos[1]+1)%self.SCREEN_HEIGHT)] == self.PIT:
            bot_vars["pit_to_south"] = 1

        return bot_vars

    @staticmethod
    def default_prog_for_bot(language):
        if language == CYLGameLanguage.LITTLEPY:
            return open("apple_bot.lp", "r").read()

    def draw_screen(self, libtcod, console):
        # End of the game
        if self.turns >= self.MAX_TURNS:
            self.running = False
            self.msgs += ["You are out of moves."]
        elif self.in_pit:
            self.running = False
            self.msgs += ["You fell into a pit :("]

        if not self.running:
            if self.apples_eaten == 0:
                self.msgs += ["You ate "+str(self.apples_eaten)+" apples. Better luck next time :("]
            else:
                self.msgs += ["You ate "+str(self.apples_eaten)+" apples. Good job!"]

        libtcod.console_set_default_foreground(console, libtcod.white)
        for pos, char in self.map.get_diff().iteritems():
            libtcod.console_put_char(console, pos[0], pos[1], char, libtcod.BKGND_NONE)
        # for x in range(self.MAP_WIDTH):
        #     for y in range(self.MAP_HEIGHT):

        # print line
        for x in range(self.SCREEN_WIDTH):
            libtcod.console_put_char(console, x, self.MAP_HEIGHT, '-')

        # print apple count
        msg_str = "Apples: " + str(self.apples_eaten)
        for i in range(len(msg_str)):
            libtcod.console_put_char(console, 2+i, self.MAP_HEIGHT + 2, msg_str[i])

        # print turn count
        msg_str = "Move: " + str(self.turns) + " of " + str(self.MAX_TURNS)
        for i in range(len(msg_str)):
            libtcod.console_put_char(console, 2+i, self.MAP_HEIGHT + 3, msg_str[i])

        for j in range(len(self.msgs[-3:])):
            # Clear msg board
            for i in range(self.MAX_MSG_LEN):
                libtcod.console_put_char(console, self.MSG_START+i, self.MAP_HEIGHT+2+j, self.EMPTY)
            # Print msg
            for i in range(min(len(self.msgs[-3:][j]), self.MAX_MSG_LEN)):
                libtcod.console_put_char(console, self.MSG_START+i, self.MAP_HEIGHT+2+j, self.msgs[-3:][j][i])


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Run: python game.py serve\n To start web server.\nRun: python game.py play\n To play on this computer.")
    elif sys.argv[1] == "serve":
        serve(AppleFinder, 'http://131.212.149.197:5000/', host='0.0.0.0')
    elif sys.argv[1] == "play":
        from CYLGameServer import CYLGameRunner
        CYLGameRunner(AppleFinder).run()
