from __future__ import print_function
import math
from CYLGame import GameLanguage
from CYLGame import Game
from CYLGame import MessagePanel
from CYLGame import MapPanel
from CYLGame import StatusPanel
from CYLGame import PanelBorder
from Bikes import *

class Tron(Game):
    MAP_WIDTH = 60
    MAP_HEIGHT = 25
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = MAP_HEIGHT + 6
    MSG_START = 20
    MAX_MSG_LEN = SCREEN_WIDTH - MSG_START - 1
    CHAR_WIDTH = 16
    CHAR_HEIGHT = 16
    GAME_TITLE = "TRON"
    CHAR_SET = "tron16x16_gs_ro.png"
    
    EMPTY = ' '

    ENEMIES = 1 # start out with 1 staticly allocated. We can move onto random as before but get to that later

    def __init__(self, random):
        self.random = random
        self.running = True
        self.enemies = self.ENEMIES       
    
        self.USER = None
        self.CORRUPTION = []

        self.turns = 0
        self.level = 0
        self.msg_panel = MessagePanel(self.MSG_START, self.MAP_HEIGHT+1, self.SCREEN_WIDTH - self.MSG_START, 5)
        self.status_panel = StatusPanel(0, self.MAP_HEIGHT+1, self.MSG_START, 5)
        self.panels = [self.msg_panel, self.status_panel]
        self.msg_panel.add("Welcome to "+self.GAME_TITLE+"!!!")
        self.msg_panel.add("Stop The Corruption")

        self.__create_map()

    def __create_map(self):
        self.map = MapPanel(0, 0, self.MAP_WIDTH, self.MAP_HEIGHT+1, self.EMPTY,
                            border=PanelBorder.create(bottom="-"))
        self.panels += [self.map]

        self.place_bikes()
        for i in self.CORRUPTION:
            self.map[i.pos()] = i.char
        self.map[self.USER.pos()] = self.USER.char
    
    def place_bikes(self):
        for i in range(0, self.ENEMIES+1):
            x = self.random.randint(0, self.MAP_WIDTH - 1)
            y = self.random.randint(0, self.MAP_HEIGHT - 1)

            if self.map[(x,y)] == self.EMPTY:
                if i == self.ENEMIES:
                    self.USER = User((x,y), chr(239))
                else:
                    self.CORRUPTION += [Computer((x,y), chr(234), self.level)]
                

    def handle_key(self, key):
        self.turns += 1
         
        if key == "w":
            self.USER.move("NORTH")
        if key == "s":
            self.USER.move("SOUTH")
        if key == "a":
            self.USER.move("WEST")
        if key == "d":
            self.USER.move("EAST")
        if key == "Q":
            self.running = False
            return
       
        self.map[self.USER.old] = self.USER.prev_char

        self.USER.x %= self.MAP_WIDTH
        self.USER.y %= self.MAP_HEIGHT

        if self.map[(self.USER.x, self.USER.y)] != ' ':
            self.running = False
        else:   
            self.map[(self.USER.x, self.USER.y)] = self.USER.char

    #    self.spread_corruption()
        
    def spread_corruption(self):
        for i in range(0, self.ENEMIES):
            cor = self.CORRUPTION[i]
            print(cor.pos())
            cor.make_move(self.map, self.MAP_WIDTH, self.MAP_HEIGHT)
            
            self.map[cor.old] = cor.prev_char
            cor.x %= self.MAP_WIDTH
            cor.y %= self.MAP_HEIGHT
            if self.map[cor.pos()] != self.EMPTY:
                for j in cor.derrezed():
                    self.map[j] = self.EMPTY
                cor = None
                del self.CORRUPTION[i]
                self.ENEMIES -= 1
                if self.ENEMIES == 0:
                    self.running = False
            else:
                self.map[cor.pos()] = cor.char

    def is_running(self):
        return self.running


    @staticmethod
    def default_prog_for_bot(language):
        if language == GameLanguage.LITTLEPY:
            return open("apple_bot.lp", "r").read()

    @staticmethod
    def get_intro():
        return open("intro.md", "r").read()

    def get_score(self):
        return self.apples_eaten

    def draw_screen(self, frame_buffer):
        # End of the game

        if not self.running:
            if self.enemies > 0:
                self.msg_panel += ["The Corruption has spread to the system. Critical Failure"]
            else:
                self.msg_panel += ["Corruption progress has stopped Exit(0)"]

        # Update Status
        self.status_panel["Enemies"] = str(self.enemies) + " left"
        self.status_panel["Turns"] = str(self.turns)
        for panel in self.panels:
            panel.redraw(frame_buffer)


if __name__ == '__main__':
    from CYLGame import run
    run(Tron)
