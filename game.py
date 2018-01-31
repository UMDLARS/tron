from __future__ import print_function
import math
from CYLGame import GridFrameBuffer
from CYLGame import GameLanguage
from CYLGame import Game
from CYLGame import MessagePanel
from CYLGame import MapPanel
from CYLGame import StatusPanel
from CYLGame import PanelBorder
from Bikes import *

class Tron(Game):
    SCREEN_WIDTH = 45
    SCREEN_HEIGHT = 30
    MAP_WIDTH = 30  #TRUE DIMENSIONS
    MAP_HEIGHT = 20 #TRUE DIMENSIONS
    MSG_START = 15
    MAX_MSG_LEN = MAP_WIDTH - MSG_START - 1
    CHAR_WIDTH = 16
    CHAR_HEIGHT = 16
    GAME_TITLE = "TRON"
    CHAR_SET = "tron16x16_gs_ro.png"
   
    TAKEN = 8912
    OPEN = 12312
    WALL = 323423
    EMPTY = ' '


    def __init__(self, random):
        self.random = random
        self.running = True
        self.DEREZZED = False
        self.NUM_ENEMIES=4
        self.enemies = self.NUM_ENEMIES
        self.USER = None
        self.sensor_coords = []
        self.CORRUPTION = []
        self.CORRUPTION_POSITIONS = [] 
        self.turns = 0
        self.level = 1
        self.msg_panel = MessagePanel(self.MSG_START, self.MAP_HEIGHT + 1, self.SCREEN_WIDTH - self.MSG_START, 5)
        self.status_panel = StatusPanel(0, self.MAP_HEIGHT+1, self.MSG_START, 5)
        self.panels = [self.msg_panel, self.status_panel]
        self.msg_panel.add("Welcome to Game GRID!!!")
        self.msg_panel.add("Stop The Corruption")

        self.__create_map()

    def __create_map(self):
        self.map = MapPanel(0, 0, self.MAP_WIDTH+2, self.MAP_HEIGHT+2, self.EMPTY,
                            border=PanelBorder.create(bottom=True, left=True, right=True, top=True))
        self.panels += [self.map]

        self.place_bikes()
        for i in self.CORRUPTION:
            self.map[i.pos()] = i.char
        self.map[self.USER.pos()] = self.USER.char
    
    def place_bikes(self):
        for i in range(0, self.NUM_ENEMIES+1):
            while True:
                x = self.random.randint(0, self.MAP_WIDTH-1)
                y = self.random.randint(0, self.MAP_HEIGHT-1)
                
                if self.map[(x,y)] == self.EMPTY:
                    if i == self.enemies:
                        self.USER = User((x,y), chr(239))
                    else:
                        self.CORRUPTION += [Computer((x,y), chr(234), self.level)]
                        self.CORRUPTION_POSITIONS += [(x,y)]
                    break;
                

    def handle_key(self, key):
        if self.DEREZZED:
            return
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
            self.DEREZZED = True
            return
        self.map[self.USER.old] = self.USER.prev_char
        if 0 >= self.USER.x or self.USER.x >= self.MAP_WIDTH:
            self.DEREZZED = True
            return
        elif 0 >=  self.USER.y or self.USER.y >= self.MAP_HEIGHT:
            self.DEREZZED = True
            return
        elif self.map[(self.USER.x, self.USER.y)] != ' ':
            self.DEREZZED = True
            return
        else:   
            self.map[(self.USER.x, self.USER.y)] = self.USER.char
        self.spread_corruption()
        
    def spread_corruption(self):
        collision = []
        for i in range(0, len(self.CORRUPTION)):
            cor = self.CORRUPTION[i]
            if cor.derezzed == True:
                continue
            cor.make_move(self.map, self.map.w, self.map.h)
            
            self.map[cor.old] = cor.prev_char
            if 0 >= cor.x or cor.x >= self.MAP_WIDTH:
                self.derezz(i)
            elif 0 >= cor.y or cor.y >= self.MAP_HEIGHT:
                self.derezz(i)
            elif cor.pos() in self.CORRUPTION_POSITIONS:
                self.derezz(i)
                self.derezz(self.CORRUPTION_POSITIONS.index(cor.pos()))
            elif cor.pos() == self.USER.pos():
                self.DEREZZED = True
                return
            elif self.map[cor.pos()] != self.EMPTY:
                self.derezz(i)
            else:
                self.map[cor.pos()] = cor.char
                self.CORRUPTION_POSITIONS[i] = cor.pos()
        if self.enemies== 0:
            self.DEREZZED = True
            return

    def derezz(self, cor_ind):
        cor = self.CORRUPTION[cor_ind]
        for j in cor.derezz():
            self.map[j] = self.EMPTY
        cor.derezzed = True
        self.enemies -= 1


    def is_running(self):
        return self.running


    @staticmethod
    def default_prog_for_bot(language):
        if language == GameLanguage.LITTLEPY:
            return open("tron.lp", "r").read()

    @staticmethod
    def get_intro():
        return open("intro.md", "r").read()

    def get_score(self):
        return self.turns + ((self.NUM_ENEMIES - self.enemies + 1) * 100)

    def draw_screen(self, frame_buffer):
        # End of the game

        if self.DEREZZED:
            if self.enemies > 0:
                self.msg_panel.add("END OF LINE")
            else:
                self.msg_panel.add("Corruption progress has stopped Exit(0)")
            self.running = False

        # Update Status
        self.status_panel["Enemies"] = str(self.enemies)
        self.status_panel["Turns"] = str(self.turns)
        for panel in self.panels:
            panel.redraw(frame_buffer)
    
    def read_bot_state(self, state):
        self.sensor_coords = []
        for i in range(8):
            x_name = "s" + str(i + 1) + "x"
            y_name = "s" + str(i + 1) + "y"
            self.sensor_coords.append((state.get(x_name, "0"), state.get(y_name, "0")))

    def get_vars_for_bot(self):
        bot_vars = {"s1": 0, "s2": 0, "s3": 0, "s4": 0, "s5": 0, "s6": 0, "s7": 0, "s8": 0}
        for i in range(0,len(self.sensor_coords)):
            x_offset = int(self.sensor_coords[i][0])
            y_offset = int(self.sensor_coords[i][1])
            if self.USER.x + x_offset > self.map.w or self.USER.x + x_offset < self.map.x:
                bot_vars["s"+str(i)] = self.WALL
            elif self.USER.y + y_offset > self.map.w or self.USER.y + y_offset < self.map.x:
                bot_vars["s"+str(i)] = self.WALL 
            else:
                if self.map[(self.USER.x + x_offset, self.USER.y + y_offset)] == ' ':
                    bot_vars["s"+str(i)] = self.OPEN
                else:
                    bot_vars["s"+str(i)] = self.TAKEN
        map_array = []
        for w in range(self.map.x, self.MAP_WIDTH):
            width_arr = []
            for h in range(self.map.y, self.MAP_HEIGHT):
                if self.map[(w, h)] == ' ':
                    width_arr.append(self.OPEN)
                else:
                    width_arr.append(self.TAKEN)
            map_array.append(tuple(width_arr))

        bot_vars["height"] = self.MAP_HEIGHT
        bot_vars["width"] = self.MAP_WIDTH

        bot_vars["map_array"] = tuple(map_array)
        return bot_vars


if __name__ == '__main__':
    from CYLGame import run
    run(Tron)
