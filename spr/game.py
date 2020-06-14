import json
from enum import Enum, auto
from collections import defaultdict
from itertools import combinations
from getpass import getpass

from .gesture_manager import GestureManager
from .player import Human, Computer


class Result(Enum):
    Win = auto()
    Draw = auto()
    Lose = auto()


class Judge():

    def __init__(self, gesture_manager):
        self._ges_manager = gesture_manager

    def _validate_gesture(self, ges):
        if ges not in self._ges_manager.available_gestures():
            raise ValueError(f"Invalid gestures {ges} ")

    def judge(self, ges1, ges2) -> Result:
        self._validate_gesture(ges1)
        self._validate_gesture(ges2)

        if ges1 == ges2:
            return Result.Draw

        loser_list = self._ges_manager.lose_to(ges1)

        return Result.Win if ges2 in loser_list else Result.Lose


class GameUI():

    output_str = {Result.Win: " beats ", Result.Draw: " draws with ",
                  Result.Lose: " lose to "}

    def __init__(self, ges_manager):
        self._ges_manager = ges_manager
        gestures = ges_manager.available_gestures()
        self._ges_dict = {i: gestures[i] for i in range(0, len(gestures))}

    def print_intro(self, name, num_games):
        print(f"{name} started, playing {num_games} rounds \n")
        print(f"Available gestures {self._ges_manager.available_gestures()}\n")
        print(f"Rules:")
        print(f"{self._ges_manager.rules_in_str()}")

    def print_result(self, player1, player2, choices, result):
        print(f"{player1} ({choices[player1]}) {self.output_str[result]}"
              f"{player2} ({choices[player2]})")

    @staticmethod
    def print_final(player_score):
        print("----------------\n")
        for player, score in player_score.items():
            print(f"{player} scored {score} ")
        print("\nGame Ended!!")

    @staticmethod
    def print_start_round(round):
        print("----------------\n")
        print(f"Round {round}")

    def get_user_choice(self, name) -> int:
        while(1):
            input_str = getpass(f"{name} enter integer of gesture"
                                f" {self._ges_dict}"
                                f" (choice will not be displayed)\n")
            index = None
            try:
                index = int(input_str)
                if index < 0 or index >= len(self._ges_dict):
                    raise ValueError("Selection not in range")
                return self._ges_dict[index]
            except ValueError:
                print(f"Invalid selection\n")


class Game():

    def __init__(self, name, num_games, judge, ges_manager, game_ui,
                 player_list):
        self._name = name
        self._num_games = num_games
        self._judge = judge
        self._ges_manager = ges_manager
        self._ui = game_ui
        self._players = player_list
        player_names = [x.name for x in self._players]
        self._player_score = defaultdict(int).fromkeys(player_names, 0)

    def _update_score(self, player1, player2, result):
        if result == Result.Win:
            self._player_score[player1] += 1
        elif result == Result.Lose:
            self._player_score[player2] += 1

    def run(self):
        self._ui.print_intro(self._name, self._num_games)

        for cur in range(self._num_games):
            self._ui.print_start_round(cur+1)

            choices = {}
            for player in self._players:
                choices[player.name] = player.get_choice()

            judge_list = combinations(choices.keys(), 2)

            for player1, player2 in judge_list:
                result = self._judge.judge(choices[player1], choices[player2])
                self._ui.print_result(player1, player2, choices, result)
                self._update_score(player1, player2, result)
        self._ui.print_final(self._player_score)


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
