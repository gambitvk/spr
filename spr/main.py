import argparse
from .game import GameCreator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scissor Paper Rock game')
    parser.add_argument('config_file', type=str, help="path to json config")
    args = parser.parse_args()

    game_creator = GameCreator(args.config_file)
    spr = game_creator.create_game()
    spr.run()
