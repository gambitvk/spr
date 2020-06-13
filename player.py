from abc import ABC, abstractmethod
import random


class Player(ABC):

    def __init__(self, name, ges_manager):
        self._name = name
        self._ges_manager = ges_manager
        super().__init__()

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_choice(self):
        pass


class Human(Player):

    def __init__(self, name, ges_manager, game_ui):
        super().__init__(name, ges_manager)
        self._ui = game_ui

    def get_choice(self):
        return self._ui.get_user_choice(self.name)


class Computer(Player):

    def get_choice(self):
        return random.choice(self._ges_manager.available_gestures())
