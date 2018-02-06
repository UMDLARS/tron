import random

import pytest
import sys

from littlepython import Compiler

from CYLGame import GameLanguage, GameRunner
from CYLGame.Player import Room
from game import Tron as Game


def get_fuzzing_seeds(new_seed_count=100):
    previous_bad_seeds = []
    return previous_bad_seeds + [random.randint(0, sys.maxsize) for _ in range(new_seed_count)]


@pytest.mark.parametrize("seed", get_fuzzing_seeds())
def test_run_for_playback(seed):
    # Make default player bot
    compiler = Compiler()
    bot = Game.default_prog_for_bot(GameLanguage.LITTLEPY)
    prog = compiler.compile(bot)

    # get computer players
    players = []
    for _ in range(Game.get_number_of_players() - 1):
        players += [Game.default_prog_for_computer()()]
    room = Room([prog] + players)

    runner = GameRunner(Game, room)
    runner.run_for_playback(seed=seed)


@pytest.mark.parametrize("seed", get_fuzzing_seeds())
def test_run_for_score(seed):
    # Make default player bot
    compiler = Compiler()
    bot = Game.default_prog_for_bot(GameLanguage.LITTLEPY)
    prog = compiler.compile(bot)

    # get computer players
    players = []
    for _ in range(Game.get_number_of_players() - 1):
        players += [Game.default_prog_for_computer()()]
    room = Room([prog] + players)

    runner = GameRunner(Game, room)
    runner.run_for_avg_score(1, seed=seed, func=sum)
