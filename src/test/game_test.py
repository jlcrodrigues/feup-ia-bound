import unittest

from model.game import Game

class TestGame(unittest.TestCase):
    def test_game_over(self):
        game = Game()
        game.board.nodes[11].place_piece(1)
        game.move((2, 1), (1, 2))
        self.assertTrue(game.over)
        self.assertEqual(game.player, 1)

if __name__ == '__main__':
    unittest.main()