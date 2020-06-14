import json

from .player import Human, Computer
from .game import GestureManager, Judge, GameUI, Game


class GameManager():

    DEFAULT_NAME = 'SPR Default'
    DEFAULT_ROUNDS = 5

    def __init__(self, config):
        with open(config) as fp:
            self._config = json.load(fp)

    def _create_gesture_manager(self):
        gesture_manager = GestureManager()
        gestures = self._config.get('gestures')
        if (gestures is None or len(gestures) == 0):
            raise ValueError('No gestures found in config')

        try:
            for gesture in gestures:
                gesture_manager.register_gesture(gesture['name'],
                                                 gesture['beats'])
        except Exception as e:
            raise ValueError(f"Malformed config file error: {e}")

        return gesture_manager

    def _create_players(self, gesture, ui):
        players = self._config.get('players')
        if (players is None or len(players) < 2):
            raise ValueError('Must define at least 2 players in config')
        player_list = []
        try:
            for player in players:
                if player['type'] == 'Human':
                    player_list.append(Human(player['name'], gesture, ui))
                elif player['type'] == 'Computer':
                    player_list.append(Computer(player['name'], gesture))
                else:
                    raise ValueError(f'Unknown player type {player["type"]}')
        except Exception as e:
            raise ValueError(f"Malformed config file error: {e}")

        return player_list

    def create_game(self):
        gesture_manager = self._create_gesture_manager()
        judge = Judge(gesture_manager)
        ui = GameUI(gesture_manager)
        players = self._create_players(gesture_manager, ui)

        game_name = self._config.get('name', self.DEFAULT_NAME)
        num_of_rounds = self._config.get('number_of_rounds',
                                         self.DEFAULT_ROUNDS)

        if num_of_rounds is None:
            num_of_rounds = 5
        return Game(game_name, num_of_rounds, judge, gesture_manager, ui,
                    players)
