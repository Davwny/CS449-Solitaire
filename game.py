
class SolitaireGame:
    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self.board = []
        self.new_game()

    def new_game(self):
        """Create a new board using the selected configuration."""
        if self.size < 5 or self.size % 2 == 0:
            raise ValueError("Board size must be odd and at least 5.")

        if self.board_type not in ("English", "Hexagon", "Diamond"):
            raise ValueError("Unknown board type.")

        center = self.size // 2
        self.board = []

        for row in range(self.size):
            board_row = []

            for col in range(self.size):
                
                if self.board_type == "English":
                    # The middle band and center columns
                    # form the traditional English cross.
                    arm_width = max(1, (self.size - 1) // 4)

                    playable = (
                        abs(row - center) <= arm_width
                        or abs(col - center) <= arm_width
                    )


    
                elif self.board_type == "Diamond":
                    playable = (
                        abs(row - center) + abs(col - center)
                        <= center
                    )

                else:  # Hexagon
                    x = row - center
                    y = col - center
                    playable = max(
                        abs(x), abs(y), abs(x + y)
                    ) <= center

                board_row.append(1 if playable else -1)

            self.board.append(board_row)

        # Start with the center hole empty.
        self.board[center][center] = 0

  
    def make_move(self, start, end):
        """Check and perform a valid move."""
        start_row, start_col = start
        end_row, end_col = end

        # Make sure both positions are on the board.
        if not all(
            0 <= value < self.size
            for value in (start_row, start_col, end_row, end_col)
        ):
            return False

        # Starting position must contain a marble.
        if self.board[start_row][start_col] != 1:
            return False

        # Destination must be an empty hole.
        if self.board[end_row][end_col] != 0:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Allow orthogonal and diagonal jumps.
        if (abs(row_diff), abs(col_diff)) not in (
            (2, 0), (0, 2), (2, 2)
        ):
            return False

        # Find the marble being jumped over.
        middle_row = start_row + row_diff // 2
        middle_col = start_col + col_diff // 2

        if self.board[middle_row][middle_col] != 1:
            return False

        # Perform the move.
        self.board[start_row][start_col] = 0
        self.board[middle_row][middle_col] = 0
        self.board[end_row][end_col] = 1

        return True


   
    def is_game_over(self):
        """Return True if no valid moves remain."""

        directions = [
            (-2, 0), (2, 0),   # Up and down
            (0, -2), (0, 2),   # Left and right
            (-2, -2), (-2, 2), # Diagonals
            (2, -2), (2, 2)
        ]

        for row in range(self.size):
            for col in range(self.size):

                if self.board[row][col] != 1:
                    continue

                for dr, dc in directions:
                    end_row = row + dr
                    end_col = col + dc

                    middle_row = row + dr // 2
                    middle_col = col + dc // 2

                    if not (
                        0 <= end_row < self.size
                        and 0 <= end_col < self.size
                    ):
                        continue

                    if (
                        self.board[middle_row][middle_col] == 1
                        and self.board[end_row][end_col] == 0
                    ):
                        return False

        return True


    def display_board(self):
        """Print the current board in the terminal."""
        for row in self.board:
            print(" ".join(
                " " if cell == -1 else str(cell)
                for cell in row
            ))



if __name__ == "__main__":
    game = SolitaireGame()

    print("Before move:")
    game.display_board()

    result = game.make_move((3, 1), (3, 3))

    print("\nMove successful:", result)
    print("\nAfter move:")
    game.display_board()

    print("\nGame over:", game.is_game_over())
    print("Marbles remaining:", sum(row.count(1) for row in game.board))