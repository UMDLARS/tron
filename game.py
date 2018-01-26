from __future__ import print_function
import math
from CYLGame import GameLanguage
from CYLGame import GridGame
from CYLGame import MessagePanel
from CYLGame import MapPanel
from CYLGame import StatusPanel
from CYLGame import PanelBorder
from Bikes import *


class Tron(GridGame):
    MAP_WIDTH = 40
    MAP_HEIGHT = 20
    SCREEN_WIDTH = 45
    SCREEN_HEIGHT = MAP_HEIGHT + 6
    MSG_START = 20
    MAX_MSG_LEN = SCREEN_WIDTH - MSG_START - 1
    CHAR_WIDTH = 16
    CHAR_HEIGHT = 16
    GAME_TITLE = "TRON"
    CHAR_SET = "tron16x16_gs_ro.png"
    MULTIPLAYER = True
    
    EMPTY = ' '


    def __init__(self, random):
        self.random = random
        self.running = True
        self.players = []
        self.num_alive = 0

        self.turns = 0
        self.level = 1
        self.msg_panel = MessagePanel(self.MSG_START, self.MAP_HEIGHT+1, self.SCREEN_WIDTH - self.MSG_START, 5)
        self.status_panel = StatusPanel(0, self.MAP_HEIGHT+1, self.MSG_START, 5)
        self.panels = [self.msg_panel, self.status_panel]
        self.msg_panel.add("Welcome to Game GRID!!!")
        self.msg_panel.add("Stop The Corruption")

    def init_board(self):
        self.map = MapPanel(0, 0, self.MAP_WIDTH, self.MAP_HEIGHT+1, self.EMPTY,
                            border=PanelBorder.create(bottom=True, left=True, right=True, top=True))
        self.panels += [self.map]

    def create_new_player(self, prog):
        self.players += [self.place_bike(prog)]
        player = self.players[-1]
        self.map[player.pos()] = player.char
        self.num_alive += 1
        return player
    
    def place_bike(self, prog):
        while True:
            x = self.random.randint(0, self.MAP_WIDTH - 1)
            y = self.random.randint(0, self.MAP_HEIGHT - 1)

            if self.map[(x, y)] == self.EMPTY:
                return Bike((x, y), chr(239), prog, self.get_move_consts())

    def do_turn(self):
        self.turns += 1
        collision = []

        self.num_alive = 0
        for player in self.players:
            if not player.derezzed:
                if player.old is not None:
                    self.map[player.old] = player.prev_char
                if player.x == self.MAP_WIDTH or player.x < 0:
                    player.derezzed = True
                elif player.y == self.MAP_HEIGHT or player.y < 0:
                    player.derezzed = True
                elif self.map[(player.x, player.y)] != ' ':
                    player.derezzed = True
                else:
                    self.map[(player.x, player.y)] = player.char
                if player.derezzed:
                    self.derezz(player)
                else:
                    self.num_alive += 1

    def derezz(self, bike):
        for j in bike.path:
            self.map[j] = self.EMPTY
        bike.derezzed = True

    def is_running(self):
        return self.running

    @staticmethod
    def default_prog_for_bot(language):
        if language == GameLanguage.LITTLEPY:
            return open("apple_bot.lp", "r").read()

    @staticmethod
    def default_prog_for_computer():
        return DumbComputer

    @staticmethod
    def get_intro():
        return open("intro.md", "r").read()

    def get_score(self):
        return self.apples_eaten

    def draw_screen(self, frame_buffer):
        # End of the game

        if self.num_alive == 1:
            self.msg_panel.add("Player {} Won!".format([x for x in range(len(self.players)) if not self.players[x].derezzed][0]))
            self.running = False
            # if self.enemies > 0:
            #     self.msg_panel += ["END OF LINE"]
            # else:
            #     self.msg_panel += ["Corruption progress has stopped Exit(0)"]
        elif self.num_alive == 0:
            self.msg_panel.add("No Player Won.")
            self.running = False

        # Update Status
        self.status_panel["Enemies"] = str(self.num_alive-1) + " left"
        self.status_panel["Turns"] = str(self.turns)
        for panel in self.panels:
            panel.redraw(frame_buffer)
    
    def get_vars_for_bot(self):
        return {}

    def get_vars(self, player):
        return {}

    @staticmethod
    def get_number_of_players():
        return 4


if __name__ == '__main__':
    from CYLGame import run
    run(Tron)
