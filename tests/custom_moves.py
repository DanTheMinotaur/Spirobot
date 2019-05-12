import unittest
from app.connect import Communicate


class TestCustomMoves(unittest.TestCase):
    def test_custom_moves_set(self):
        static_move_names = [
            "walk1",
            "walk2",
            "jump"
        ]
        c = Communicate()
        moves = c.set_custom_moves(static_move_names)
        print(moves)


if __name__ == '__main__':
    unittest.main()