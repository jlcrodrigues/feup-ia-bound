import unittest
import sys

sys.path.insert(0, '../src')

from model.board import Board, Node

# The unit test class
class TestBoard(unittest.TestCase):
    def test_generate_small(self):
        board = Board(2, 3)

        sample_nodes = [Node(0, 0, set([1, 2, 3])), Node(0, 1, set([0, 2, 4])), Node(0, 2, set([0, 1, 5])),
                         Node(1, 0, set([5, 4, 0])), Node(1, 1, set([3, 5, 1])), Node(1, 2, set([3, 4, 2]))]

        self.assertEqual(board.nodes, sample_nodes)

    def test_generate_normal(self):
        board = Board()

        sample_nodes = [Node(0, 0, set([1, 4, 5])), Node(0, 1, set([0, 2, 6])), Node(0, 2, set([7, 1, 3])), Node(0, 3, set([4, 2, 8])),Node(0, 4, set([0, 9, 3])),
                         Node(1, 0, set([10, 14, 0])), Node(1, 1, set([10, 11, 1])), Node(1, 2, set([11, 12, 2])), Node(1, 3, set([3, 13, 12])), Node(1, 4, set([13, 4, 14])),
                         Node(2, 0, set([15, 5, 6])), Node(2, 1, set([6, 7, 16])), Node(2, 2, set([7, 8, 17])), Node(2, 3, set([9, 8, 18])), Node(2, 4, set([19, 5, 9])),
                         Node(3, 0, set([10, 19, 16])), Node(3, 1, set([11, 15, 17])), Node(3, 2, set([16, 18, 12])), Node(3, 3, set([19, 13, 17])), Node(3, 4, set([14, 15, 18]))
                         ]

        self.assertEqual(board.nodes, sample_nodes)

if __name__ == '__main__':
    unittest.main()