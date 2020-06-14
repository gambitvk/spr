import argparse
from .game_manager import GameManager


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scissor Paper Rock game')
    parser.add_argument('config_file', type=str, help="path to json config")
    args = parser.parse_args()

    game_manager = GameManager(args.config_file)
    spr = game_manager.create_game()
    spr.run()
