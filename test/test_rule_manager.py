from unittest import TestCase
# from unittest.mock import patch
# from io import StringIO

from spr.game import RuleManager, Result


class TestRuleManager(TestCase):

    def setUp(self):
        self.rock = 'Rock'
        self.scissor = 'Scissor'
        self.paper = 'Paper'

        config = {
            "gestures": [
                {
                    "name": self.rock,
                    "beats": [self.scissor]
                },
                {
                    "name": self.scissor,
                    "beats": [self.paper]
                },
                {
                    "name": self.paper,
                    "beats": [self.rock]
                }
            ]
        }
        self.rule_manager = RuleManager(config)

    def test_available_gestures(self):
        expected = [self.rock, self.scissor, self.paper]

        result = self.rule_manager.available_gestures()

        self.assertCountEqual(expected, result)

    def test_judge_invalid_gestures(self):
        invalid_gestures = 'wrong'

        self.assertRaises(ValueError, self.rule_manager.judge, self.rock,
                          invalid_gestures)

    def test_judge_valid_gestures_draw(self):
        expected = Result.Draw

        result = self.rule_manager.judge(self.rock, self.rock)

        self.assertEqual(expected, result)

    def test_judge_valid_gestures_win(self):
        expected = Result.Win

        result = self.rule_manager.judge(self.rock, self.scissor)

        self.assertEqual(expected, result)

    def test_judge_valid_gestures_lose(self):
        expected = Result.Lose

        result = self.rule_manager.judge(self.rock, self.paper)

        self.assertEqual(expected, result)
