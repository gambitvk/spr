import json
from enum import Enum, auto
from collections import defaultdict
from itertools import combinations
from typing import Dict, List
from getpass import getpass

from .player import PlayerCreator, Player


class Result(Enum):
    """
    A class to model all possible results
    """

    Win = auto()
    Draw = auto()
    Lose = auto()


class RuleManager():
    """
    RuleManager class keep tracks of gestures and their relationship (rules)
    """

    def __init__(self, config: dict) -> None:
        """
        Takes a dictionary assuming its parsed from a Json config file

        ...

        Config example:

        {
            "gestures":[
                {
                    "name": "Rock",
                    "beats": ["Paper"]
                }
            ]
        }

        """
        self._gestures = []
        self._lose_to = {}
        self._import_config(config)

    def _import_config(self, config: dict) -> None:
        gestures = config.get('gestures')
        if (gestures is None or len(gestures) == 0):
            raise ValueError('No gestures found in config')
        try:
            for gesture in gestures:
                self._register_gesture(gesture['name'], gesture['beats'])
        except Exception as e:
            raise ValueError(f"Malformed config file error: {e}")

    def _register_gesture(self, gesture: str, lose_to: List[str]) -> None:
        self._gestures.append(gesture)
        self._lose_to[gesture] = lose_to

    def available_gestures(self) -> List[str]:
        """
        Return a list of gesture's name

            Returns examples: ["Rock", "Scissor", "Paper"]

        """

        return self._gestures

    def rules_in_str(self) -> str:
        """
        Returns a long string of the registered rules

            Returns example:
                "Rock bests ['Scissor']"
        """

        result = []
        for gesture, lose_to in self._lose_to.items():
            result.append(f"{gesture} beats {lose_to}")
        return "\n".join(result)

    def _validate_gesture(self, ges: str) -> None:
        if ges not in self._gestures:
            raise ValueError(f"Invalid gestures {ges} ")

    def judge(self, ges1: str, ges2: str) -> Result:
        self._validate_gesture(ges1)
        self._validate_gesture(ges2)

        if ges1 == ges2:
            return Result.Draw

        loser_list = self._lose_to[ges1]

        return Result.Win if ges2 in loser_list else Result.Lose


class GameUI():
    """
    A class that deals with input from user and displaying output
    """

    output_str = {Result.Win: " beats ", Result.Draw: " draws with ",
                  Result.Lose: " lose to "}

    def __init__(self, game_name: str) -> None:
        """
        Contructs the GameUI object

            Param:
                game_name: str - Name to the game for displaying  purpose
        """

        self._name = game_name

    def print_intro(self, num_games: int, rules: str,
                    gestures: List[str]) -> None:
        print(f"{self._name} started, playing {num_games} rounds \n")
        print(f"Available gestures {gestures}\n")
        print(f"Rules:")
        print(f"{rules}")

    def print_result(self, player1: str, player2: str, choices: Dict[str, str],
                     result: Result) -> None:
        print(f"{player1} ({choices[player1]}) {self.output_str[result]}"
              f"{player2} ({choices[player2]})")

    @staticmethod
    def print_final(player_score: Dict[str, int]) -> None:
        print("----------------\n")
        for player, score in player_score.items():
            print(f"{player} scored {score} ")
        print("\nGame Ended!!")

    @staticmethod
    def print_start_round(round: int) -> None:
        print("----------------\n")
        print(f"Round {round}")

    @staticmethod
    def get_user_choice(user_name: str, choices: dict) -> str:
        return getpass(f"{user_name} enter number next to gesture "
                       f"{choices} "
                       f"(choice enterted is hidden)\n")


class Game():
    """
    A class that present the main logic of a Game

    Methods:

        run():
            Starts the game's main loop
    """

    def __init__(self, num_games: int, rule_manager: RuleManager,
                 game_ui: GameUI, player_list: List[Player]) -> None:
        """
        Construct a game object

        Param:
            num_games: int
                number of rounds to play
            rule_manager: RuleManager
                RuleManager object contains rules and gestures, which it use to
                determine who wins each round
            game_ui: GameUI
                GameUI onbjects help display messages and instruction of the
                game to user
            player_list: Listp[Player]
                List of player participating the game

        """

        self._num_games = num_games
        self._rule_manager = rule_manager
        self._ui = game_ui
        self._players = player_list
        player_names = [x.name for x in self._players]
        self._player_score = defaultdict(int).fromkeys(player_names, 0)
        self._judge_list = [x for x in combinations(player_names, 2)]

    def _update_score(self, player1: str, player2: str, result: Result):
        if result == Result.Win:
            self._player_score[player1] += 1
        elif result == Result.Lose:
            self._player_score[player2] += 1

    def run(self) -> None:
        """
        Starts the main loop for the game
        """
        self._ui.print_intro(self._num_games,
                             self._rule_manager.rules_in_str(),
                             self._rule_manager.available_gestures())

        for cur in range(self._num_games):
            self._ui.print_start_round(cur+1)

            choices = {p.name: p.get_choice() for p in self._players}

            for (player1, player2) in self._judge_list:
                result = self._rule_manager.judge(choices[player1],
                                                  choices[player2])
                self._ui.print_result(player1, player2, choices, result)
                self._update_score(player1, player2, result)
        self._ui.print_final(self._player_score)


class GameCreator():
    """
    A class that deals with creating a game. It deals with handling the json
    config file and create all the necessary dependent objects

    Methods:

        create_game() -> Game
            Returns a fully configure Game object
    """

    DEFAULT_NAME = 'SPR Default'
    DEFAULT_ROUNDS = 5

    def __init__(self, config: str):
        """
        Initialize  the GameCreator

        Parms:
            config: str
                full filepath of the json config file
        """

        with open(config) as fp:
            self._config = json.load(fp)

    def create_game(self) -> Game:
        """
        Returns a fully configure Game object base on config file

        Returns:
            Game
        """

        game_name = self._config.get('name', self.DEFAULT_NAME)
        ui = GameUI(game_name)

        rule_manager = RuleManager(self._config)

        players = PlayerCreator.create(self._config, gestures=rule_manager.
                                       available_gestures(),
                                       get_user_choice_fn=ui.get_user_choice)

        num_of_rounds = self._config.get('number_of_rounds',
                                         self.DEFAULT_ROUNDS)

        return Game(num_of_rounds, rule_manager, ui, players)
