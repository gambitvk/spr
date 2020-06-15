from abc import ABC, abstractmethod
from getpass import getpass
import random
from typing import List


class Player(ABC):

    def __init__(self, name: str, gestures: List[str]) -> None:
        self._name = name
        self._gestures = gestures
        super().__init__()

    @property
    def name(self) -> None:
        return self._name

    @abstractmethod
    def get_choice(self) -> str:
        pass


class Human(Player):

    def __init__(self, name: str, gestures: List[str]) -> None:
        super().__init__(name, gestures)
        self._ges_dict = {index: elem for index, elem in enumerate(gestures)}

    def get_choice(self) -> int:
        while(1):
            input_str = getpass(f"{self._name} enter integer of gesture "
                                f"{self._ges_dict} "
                                f"(choice will not be displayed)\n")
            index = None
            try:
                index = int(input_str)
                if index < 0 or index >= len(self._ges_dict):
                    raise ValueError("Selection not in range")
                return self._ges_dict[index]
            except ValueError:
                print(f"Invalid selection\n")


class Computer(Player):

    def get_choice(self) -> str:
        return random.choice(self._gestures)


class PlayerCreator():

    _creators = {'Human': Human, 'Computer': Computer}

    @classmethod
    def _create(cls, player, **kwargs):
        key = player['type']
        creator = cls._creators.get(key)
        if not creator:
            raise ValueError(f"Unknown Player type {key}")

        return creator(player['name'], **kwargs)

    @classmethod
    def create(cls, config: dict, **kwargs) -> list:
        players = config.get('players')
        if (not players or len(players) < 2):
            raise ValueError('Must define at least 2 players in config')

        try:
            return [cls._create(player, **kwargs) for player in players]
        except Exception as e:
            raise ValueError(f"Malformed config file error: {e}")
