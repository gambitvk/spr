from unittest import TestCase
from unittest.mock import patch, Mock
from io import StringIO


from spr.player import Human, Computer


class TestPlayer(TestCase):

    def setUp(self):
        self.gestures = ['Rock', 'Scissor', 'Paper']
        self.get_user_fn = Mock()
        self.human = Human('human', self.gestures, self.get_user_fn)
        self.computer = Computer('computer', self.gestures)

    @patch('sys.stdout', new_callable=StringIO)
    def test_human_get_choice_invalid(self, mock_stdout):
        invalid_index = 10
        valid_index = 1
        self.get_user_fn.side_effect = [invalid_index, valid_index]
        expected_stdout = 'Invalid selection'
        expected_result = self.gestures[valid_index]

        result = self.human.get_choice()

        self.assertEqual(mock_stdout.getvalue().strip(), expected_stdout)
        self.assertEqual(expected_result, result)

    def test_human_get_choice_valid(self):
        index = 2
        self.get_user_fn.side_effect = [index]
        expected = self.gestures[index]

        result = self.human.get_choice()

        self.assertEqual(expected, result)

    def test_computer_get_choice(self):
        expected = self.gestures
        result = self.computer.get_choice()

        self.assertTrue(result in expected)
