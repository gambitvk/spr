import argparse
import json

from player import Human, Computer
from game import GestureManager, Judge, GameUI, Game


def create_gesture_manager(config):
    gesture_manager = GestureManager()
    if len(config['gestures']) == 0:
        raise ValueError('No gestures found in config')

    for gesture in config['gestures']:
        gesture_manager.register_gesture(gesture['name'],
                                         gesture['beats'])
    return gesture_manager


def create_players(config, gesture, ui):
    if len(config['players']) < 2:
        raise ValueError('Must define at least 2 players in  config')
    player_list = []
    for player in config['players']:
        if player['type'] == 'Human':
            player_list.append(Human(player['name'], gesture, ui))
        elif player['type'] == 'Computer':
            player_list.append(Computer(player['name'], gesture))
        else:
            raise ValueError(f'Unknown player type {player["type"]}')

    return player_list


def init(config):
    gesture_manager = create_gesture_manager(config)
    judge = Judge(gesture_manager)
    ui = GameUI(gesture_manager)
    players = create_players(config, gesture_manager, ui)

    return Game(config['name'], config['number_of_rounds'], judge,
                gesture_manager, ui, players)


def parse_config(path):
    with open(path) as fp:
        return json.load(fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scissor Paper Rock game')
    parser.add_argument('config_file', type=str, help="path to json config")
    args = parser.parse_args()

    config_json = parse_config(args.config_file)
    spr = init(config_json)
    spr.run()
