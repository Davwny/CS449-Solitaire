
import tkinter as tk
from tkinter import ttk, messagebox
from game import SolitaireGame


class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CS449 Peg Solitaire")

        self.game = SolitaireGame()
        self.selected = None

        # Board configuration controls
        controls = ttk.Frame(root, padding=10)
        controls.pack()

        ttk.Label(controls, text="Board Size:").pack(side="left")

        self.size_var = tk.StringVar(value="7")
        ttk.Combobox(
            controls,
            textvariable=self.size_var,
            values=["5", "7", "9"],
            width=5,
            state="readonly"
        ).pack(side="left", padx=5)

        ttk.Label(controls, text="Board Type:").pack(side="left")

        self.type_var = tk.StringVar(value="English")
        ttk.Combobox(
            controls,
            textvariable=self.type_var,
            values=["English", "Hexagon", "Diamond"],
            width=12,
            state="readonly"
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="New Game",
            command=self.new_game
        ).pack(side="left", padx=10)

        # Board area
        self.board_frame = ttk.Frame(root, padding=15)
        self.board_frame.pack()

        self.status_var = tk.StringVar()
        ttk.Label(
            root,
            textvariable=self.status_var
        ).pack(pady=10)

        self.draw_board()

    def new_game(self):
        size = int(self.size_var.get())
        board_type = self.type_var.get()

        self.game = SolitaireGame(size, board_type)
        self.selected = None
        self.draw_board()

    def draw_board(self):
        # Remove old buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for row in range(self.game.size):
            for col in range(self.game.size):
                value = self.game.board[row][col]

                if value == -1:
                    continue

                if value == 1:
                    symbol = "●"
                else:
                    symbol = "○"

                color = (
                    "lightblue"
                    if self.selected == (row, col)
                    else "white"
                )

                
                is_selected = self.selected == (row, col)

                button = tk.Button(
                    self.board_frame,
                    text=symbol,
                    width=3,
                    height=1,
                    font=("Arial", 18, "bold"),
                    bg="yellow" if is_selected else "white",
                    fg="blue" if is_selected else "black",
                    relief="sunken" if is_selected else "raised",
                    command=lambda r=row, c=col:
                        self.click_cell(r, c)
                )

                button.grid(row=row, column=col)


        marbles = sum(
            row.count(1) for row in self.game.board
        )

        self.status_var.set(
            f"Marbles remaining: {marbles}"
        )

    
    def click_cell(self, row, col):
        print(f"Clicked: ({row}, {col})")

        # First click: select a marble
        if self.selected is None:
            if self.game.board[row][col] == 1:
                self.selected = (row, col)
                print("Selected marble:", self.selected)
                self.draw_board()
            return

        # Click the same marble to deselect it
        if self.selected == (row, col):
            self.selected = None
            self.draw_board()
            return

        # Click another marble to change selection
        if self.game.board[row][col] == 1:
            self.selected = (row, col)
            self.draw_board()
            return

        # Second click: attempt the move
        start = self.selected
        self.selected = None

        if self.game.make_move(start, (row, col)):
            print("Move successful!")
            self.draw_board()

            if self.game.is_game_over():
                messagebox.showinfo(
                    "Game Over",
                    "No more valid moves!"
                )
        else:
            print("Invalid move!")
            self.draw_board()



if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
