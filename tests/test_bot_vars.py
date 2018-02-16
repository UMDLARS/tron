from CYLGame.Player import Prog
from pytest_mock import mocker

from game import Tron, Bike


class MockProg(Prog):
    def __init__(self):
        self.key = None
        self.state = {}
        self.options = {}
        self.last_state = None

    def run(self, state=None, **kwargs):
        self.last_state = state
        state = dict(self.state)
        state["move"] = ord(self.key)
        return state


def make_tron_map(game, player_pos, *paths):
    map_array = []
    for w in range(0, game.MAP_WIDTH):
        width_arr = []
        for h in range(0, game.MAP_HEIGHT):
            width_arr.append(game.OPEN)
        map_array.append(list(width_arr))
    map_array[player_pos[0]][player_pos[1]] = game.TAKEN
    for spot in paths:
        map_array[spot[0]][spot[1]] = game.TAKEN
    return map_array


def make_tron_sensors(game, player, default=None, **kargs):
    if default is None:
        default = game.OPEN
    d = {}
    for i in range(player.NUM_OF_SENSORS):
        d["s{}".format(i+1)] = default
    d.update(kargs)
    return d


def test_start_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"
    vars = game.get_vars(player)
    correct_vars = {**make_tron_sensors(game, player, default=0),
                    "height": game.MAP_HEIGHT, "width": game.MAP_WIDTH}
    correct_vars["map"] = make_tron_map(game, (x, y))

    assert vars == correct_vars
    # player.run_turn(None)
    # prog.last_state == {}
    # game.do_turn()


def test_start_vars_2(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 4, 5
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"
    vars = game.get_vars(player)
    correct_vars = {**make_tron_sensors(game, player, default=0),
                    "height": game.MAP_HEIGHT, "width": game.MAP_WIDTH}
    correct_vars["map"] = make_tron_map(game, (x, y))

    assert vars == correct_vars


def test_move_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 4, 5
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN),
                    "height": game.MAP_HEIGHT, "width": game.MAP_WIDTH}
    correct_vars["map"] = make_tron_map(game, (x+1, y), (x, y))

    assert vars == correct_vars


def test_wall_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 1, 1
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": -1}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.WALL),
                    "height": game.MAP_HEIGHT, "width": game.MAP_WIDTH}
    correct_vars["map"] = make_tron_map(game, (x+1, y), (x, y))

    assert vars == correct_vars
