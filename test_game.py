
import unittest
from game import SolitaireGame


class TestSolitaireGame(unittest.TestCase):

    def test_new_game(self):
        """Test that a new game has an empty center."""
        game = SolitaireGame(7, "English")

        self.assertEqual(game.board[3][3], 0)
        self.assertEqual(game.board[3][2], 1)

    def test_valid_move(self):
        """Test a legal marble jump."""
        game = SolitaireGame(7, "English")

        result = game.make_move((3, 1), (3, 3))

        self.assertTrue(result)
        self.assertEqual(game.board[3][1], 0)
        self.assertEqual(game.board[3][2], 0)
        self.assertEqual(game.board[3][3], 1)

    def test_invalid_move(self):
        """Test that an invalid move is rejected."""
        game = SolitaireGame(7, "English")

        result = game.make_move((3, 2), (3, 3))

        self.assertFalse(result)
        self.assertEqual(game.board[3][3], 0)

    def test_game_not_over(self):
        """Test that a new game has legal moves."""
        game = SolitaireGame(7, "English")

        self.assertFalse(game.is_game_over())

    def test_game_over(self):
        """Test a board with no remaining moves."""
        game = SolitaireGame(7, "English")

        for row in range(game.size):
            for col in range(game.size):
                if game.board[row][col] != -1:
                    game.board[row][col] = 0

        game.board[3][3] = 1

        self.assertTrue(game.is_game_over())


    def test_english_board_shape(self):
        game = SolitaireGame(7, "English")

        playable = sum(
            cell != -1
            for row in game.board
            for cell in row
        )

        self.assertEqual(playable, 33)
        self.assertEqual(game.board[3][3], 0)
        self.assertEqual(game.board[0][0], -1)

    def test_diamond_board_shape(self):
        game = SolitaireGame(7, "Diamond")

        playable = sum(
            cell != -1
            for row in game.board
            for cell in row
        )

        self.assertEqual(playable, 25)
        self.assertEqual(game.board[3][3], 0)

    def test_hexagon_board_shape(self):
        game = SolitaireGame(7, "Hexagon")

        playable = sum(
            cell != -1
            for row in game.board
            for cell in row
        )

        self.assertEqual(playable, 37)
        self.assertEqual(game.board[3][3], 0)

    def test_all_board_sizes(self):
        for board_type in ("English", "Diamond", "Hexagon"):
            for size in (5, 7, 9):
                with self.subTest(
                    board_type=board_type,
                    size=size
                ):
                    game = SolitaireGame(size, board_type)

                    self.assertEqual(len(game.board), size)
                    self.assertTrue(
                        all(len(row) == size for row in game.board)
                    )
                    self.assertEqual(
                        game.board[size // 2][size // 2],
                        0
                    )


    
if __name__ == "__main__":
    unittest.main()