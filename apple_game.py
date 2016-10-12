from __future__ import print_function
import sys
import random
from CYLGameServer import serve
from CYLGameServer import CYLGameLanguage
from CYLGameServer import CYLGame


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
    MAX_TURNS = 99

    PLAYER = '@'
    APPLE = 'O'
    EMPTY = ' '

    def __init__(self):
        self.running = True
        centerx = self.MAP_WIDTH / 2
        centery = self.MAP_HEIGHT / 2
        self.player_pos = [centerx, centery]
        self.apples_eaten = 0
        self.apples_left = 0
        self.turns = 0
        self.msgs = ["Welcome to "+self.GAME_TITLE+"!!!", "Try to eat as many apples as possible"]

        self.__create_map()

    def __create_map(self):
        self.map = [[self.EMPTY] * self.MAP_WIDTH for _ in range(self.MAP_HEIGHT)]

        self.map[self.player_pos[1]][self.player_pos[0]] = self.PLAYER

        self.place_apples(self.NUM_OF_APPLES)

    def place_apples(self, count):
        placed_apples = 0
        while placed_apples < count:
            x = random.randint(0, self.MAP_WIDTH - 1)
            y = random.randint(0, self.MAP_HEIGHT - 1)

            if self.map[y][x] == self.EMPTY:
                self.map[y][x] = self.APPLE
                placed_apples += 1
        self.apples_left = self.apples_left + count

    def handle_key(self, key):
        self.turns += 1
        if self.turns > self.MAX_TURNS:
            self.running = False
            return

        self.map[self.player_pos[1]][self.player_pos[0]] = self.EMPTY
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
        if self.map[self.player_pos[1]][self.player_pos[0]] == self.APPLE:
            self.apples_eaten += 1
            self.apples_left -= 1
            self.msgs += [random.choice(list(set(self.APPLE_EATING_RESPONSES)-set(self.msgs[-3:])))]
        self.map[self.player_pos[1]][self.player_pos[0]] = self.PLAYER

        if self.apples_left == 0:
            self.place_apples(self.NUM_OF_APPLES)

    def is_running(self):
        return self.running

    def find_closest_apple(self, x, y):
        visited_pos = []
        nodes = [(0, None, x, y)]
        visited_pos = [[x, y]]
        while len(nodes):
            nodes.sort()
            node = nodes.pop(0)
            dist, dir, x, y = node

            if self.map[y][x] == self.APPLE:
                return dir
            for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if not node[1]:
                    dir = d
                new_node = [node[0]+1, dir, node[2]+d[0], node[3]+d[1]]
                new_node[2] %= self.MAP_WIDTH
                new_node[3] %= self.MAP_HEIGHT
                if new_node[-2:] not in visited_pos:
                    nodes += [new_node]
                    visited_pos += [new_node[-2:]]
        raise Exception("We didn't find an apple")
        # return 0, 0

    def get_vars_for_bot(self):
        bot_vars = {}

        # get closest apple
        spots = []
        # while spots
        x_dir, y_dir = self.find_closest_apple(*self.player_pos)

        x_dir_to_char = {-1: ord("a"), 1: ord("d"), 0: 0}
        y_dir_to_char = {-1: ord("w"), 1: ord("s"), 0: 0}

        bot_vars = {"x_dir": x_dir_to_char[x_dir], "y_dir": y_dir_to_char[y_dir]}

        return bot_vars

    @staticmethod
    def default_prog_for_bot(language):
        if language == CYLGameLanguage.LITTLEPY:
            return open("apple_bot.lp", "r").read()

    def draw_screen(self, libtcod, console):
        # self.msgs += ["Dist to closest apple: " + str(self.find_closest_apple(*self.player_pos))]
        libtcod.console_set_default_foreground(console, libtcod.white)
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                libtcod.console_put_char(console, x, y, self.map[y][x], libtcod.BKGND_NONE)

        # print line
        for x in range(self.SCREEN_WIDTH):
            libtcod.console_put_char(console, x, self.MAP_HEIGHT, '-')

        # print apple count
        msg_str = "Apples: " + str(self.apples_eaten)
        for i in range(len(msg_str)):
            libtcod.console_put_char(console, 2+i, self.MAP_HEIGHT + 2, msg_str[i])

        for j in range(len(self.msgs[-3:])):
            # Clear msg board
            for i in range(self.MAX_MSG_LEN):
                libtcod.console_put_char(console, self.MSG_START+i, self.MAP_HEIGHT+2+j, self.EMPTY)
            # Print msg
            for i in range(min(len(self.msgs[-3:][j]), self.MAX_MSG_LEN)):
                libtcod.console_put_char(console, self.MSG_START+i, self.MAP_HEIGHT+2+j, self.msgs[-3:][j][i])


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Run: python game.py serve\nTo start web server.\nRun: python game.py play\n To play on this computer.")
    if sys.argv[1] == "serve":
        serve(AppleFinder)
    elif sys.argv[1] == "play":
        from CYLGameServer import CYLGameRunner
        CYLGameRunner(AppleFinder).run()
