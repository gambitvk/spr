from unittest import TestCase
from unittest.mock import patch
from io import StringIO


from spr.player import Human, Computer


class TestPlayer(TestCase):

    def setUp(self):
        self.gestures = ['Rock', 'Scissor', 'Paper']
        self.human = Human('human', self.gestures)
        self.computer = Computer('computer', self.gestures)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('spr.player.getpass')
    def test_human_get_choice_invalid(self, mock_getpass, mock_stdout):
        invalid_index = 10
        valid_index = 1
        mock_getpass.side_effect = [invalid_index, valid_index]
        expected_stdout = 'Invalid selection'
        expected_result = self.gestures[valid_index]

        result = self.human.get_choice()

        self.assertEqual(mock_stdout.getvalue().strip(), expected_stdout)
        self.assertEqual(expected_result, result)

    @patch('spr.player.getpass')
    def test_human_get_choice_valid(self, mock_getpass, ):
        index = 2
        mock_getpass.side_effect = [index]
        expected = self.gestures[index]

        result = self.human.get_choice()

        self.assertEqual(expected, result)

    def test_computer_get_choice(self):
        expected = self.gestures
        result = self.computer.get_choice()

        self.assertTrue(result in expected)
