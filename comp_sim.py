#!/usr/bin/python
import sys
from game import Tron
from littlepython import Compiler
from CYLGame.Database import GameDB
from CYLGame.Comp import MultiplayerComp


#
# comp_token = sys.argv[1]
# game = AppleFinder
# compiler = Compiler()
# gamedb = GameDB(sys.argv[2])
# assert gamedb.is_comp_token(comp_token)
#
# sim_competition(compiler=compiler, game=game, gamedb=gamedb, token=comp_token, runs=100, debug=True)


#def sim_multiplayer(s_token, gamedb, game, compiler, debug=False):

s_token = 'S2ACBA9ED'
game = Tron
compiler = Compiler()
gamedb = GameDB("temp_game")
MultiplayerComp.sim_multiplayer(s_token, gamedb, game, compiler)

