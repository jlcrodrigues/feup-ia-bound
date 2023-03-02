import unittest

from model.game import Game

class TestGame(unittest.TestCase):
    def test_game_over(self):
        game = Game()
        game.board.place_piece(1, (2, 1))
        game.move((2, 1), (1, 2))
        self.assertTrue(game.over)
        self.assertEqual(game.player, 1)

    def test_not_game_over(self):
        game = Game()
        game.move((3, 2), (2, 2))
        game.move((0, 2), (1, 2))
        self.assertFalse(game.over)

if __name__ == '__main__':
    unittest.main()