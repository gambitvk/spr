from enum import Enum, auto
from collections import defaultdict
from itertools import combinations
from getpass import getpass


class Result(Enum):
    Win = auto()
    Draw = auto()
    Lose = auto()


class GestureManager():

    def __init__(self):
        self._gestures = []
        self._lose_to = {}

    def register_gesture(self, gesture, lose_to):
        self._gestures.append(gesture)
        self._lose_to[gesture] = lose_to

    def available_gestures(self):
        return self._gestures

    def rules_in_str(self):
        result = []
        for gesture, lose_to in self._lose_to.items():
            result.append(f"{gesture} defects {lose_to}")
        return "\n".join(result)

    def lose_to(self, gesture):
        return self._lose_to[gesture]


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
        self._player_score = defaultdict(int)

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
