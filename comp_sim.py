#!/usr/bin/python
import sys
from game import Tron
from littlepython import Compiler
from CYLGame.Database import GameDB
from CYLGame.Comp import MultiplayerComp


c_token = sys.argv[1]
game = Tron
compiler = Compiler()
gamedb = GameDB(sys.argv[2])
MultiplayerComp.sim_comp(c_token, gamedb, game, compiler, debug=True)

