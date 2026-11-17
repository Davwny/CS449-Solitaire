
import tkinter as tk
from tkinter import ttk, messagebox
from game import SolitaireGame


class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CS449 Peg Solitaire")

        self.game = SolitaireGame()
        self.selected = None
        self.record_var = tk.BooleanVar(value=False)


        # Track automated actions
        self.is_autoplaying = False
        self.is_replaying = False
        self.scheduled_job = None


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


        ttk.Button(
            controls,
            text="Autoplay",
            command=self.start_autoplay
        ).pack(side="left", padx=5)

       
        ttk.Button(
            controls,
            text="Randomize",
            command=self.randomize_game
        ).pack(side="left", padx=5)
 

        ttk.Button(
            controls,
            text="Replay",
            command=self.start_replay
        ).pack(side="left", padx=5)


        ttk.Checkbutton(
            controls,
            text="Record Game",
            variable=self.record_var,
            command=self.toggle_recording
        ).pack(side="left", padx=5)




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
        """Start a new game and stop automated actions."""


        # Prevent losing an active recording
        if self.record_var.get():
            messagebox.showwarning(
                "Recording Active",
                "Stop and save your recording before starting a new game."
            )
            return


        self.stop_automated_actions()

        size = int(self.size_var.get())
        board_type = self.type_var.get()

        self.game = SolitaireGame(size, board_type)
        self.selected = None

        # Preserve recording when starting a new game
        self.game.recording = self.record_var.get()

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
        if self.is_autoplaying or self.is_replaying:
            return
        
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




    def randomize_game(self):
        if self.is_autoplaying or self.is_replaying:
            return
        

        """Randomize the current game board."""
        self.selected = None

        moves = self.game.randomize_board(3)

        self.draw_board()

        if moves == 0:
            messagebox.showinfo(
                "Game Over",
                "No more valid moves!"
            )
        elif self.game.is_game_over():
            messagebox.showinfo(
                "Game Over",
                "Randomization completed. No moves remain!"
            )

        


    
    def start_autoplay(self):
        """Start automated gameplay safely."""

        if self.is_autoplaying or self.is_replaying:
            return

        self.is_autoplaying = True
        self.selected = None
        self.play_auto_step()

    def play_auto_step(self):
        """Perform one automatic move."""

        if not self.is_autoplaying:
            return

        self.scheduled_job = None

        if self.game.auto_move():
            self.draw_board()

            self.scheduled_job = self.root.after(
                300, self.play_auto_step
            )
        else:
            self.stop_automated_actions()
            self.draw_board()

            marbles = sum(
                row.count(1) for row in self.game.board
            )

            messagebox.showinfo(
                "Autoplay Complete",
                f"Game over! Marbles remaining: {marbles}"
            )


    
    def start_replay(self):
        """Load and visually replay a recorded game."""

        if self.is_autoplaying or self.is_replaying:
            return

        if self.record_var.get():
            messagebox.showwarning(
                "Recording Active",
                "Stop recording before starting Replay."
            )
            return

        try:
            self.game.load_game("recorded_game.json")
        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror("Replay Error", str(error))
            return

        self.is_replaying = True
        self.selected = None
        self.replay_moves = list(self.game.move_history)
        self.replay_index = 0

        self.draw_board()

        self.scheduled_job = self.root.after(
            500, self.play_replay_step
        )

    def play_replay_step(self):
        """Replay recorded moves one at a time."""

        if not self.is_replaying:
            return

        self.scheduled_job = None

        if self.replay_index >= len(self.replay_moves):
            self.stop_automated_actions()

            messagebox.showinfo(
                "Replay Complete",
                "All recorded moves have been replayed!"
            )
            return

        move = self.replay_moves[self.replay_index]

        try:
            start = tuple(move["start"])
            end = tuple(move["end"])

            if not self.game.make_move(start, end):
                raise ValueError(
                    f"Invalid recorded move: {start} -> {end}"
                )

        except (KeyError, TypeError, ValueError, IndexError) as error:
            self.stop_automated_actions()
            messagebox.showerror("Replay Error", str(error))
            return

        self.replay_index += 1
        self.draw_board()

        self.scheduled_job = self.root.after(
            500, self.play_replay_step
        )


    def toggle_recording(self):
        """Start or stop recording the current game."""

        if self.is_autoplaying or self.is_replaying:
            self.record_var.set(self.game.recording)

            messagebox.showwarning(
                "Game Busy",
                "Wait until Autoplay or Replay finishes."
            )
            return

        
        if self.record_var.get():
            # Start recording from a fresh board.
            size = int(self.size_var.get())
            board_type = self.type_var.get()

            self.game = SolitaireGame(size, board_type)
            self.selected = None
            self.game.move_history = []
            self.game.recording = True
            self.draw_board()


            messagebox.showinfo(
                "Recording Started",
                "Your game is now being recorded."
            )

        else:
            # Stop recording and save the game.
            self.game.recording = False

            try:
                self.game.save_game("recorded_game.json")
                messagebox.showinfo(
                    "Recording Saved",
                    "Game saved to recorded_game.json"
                )
            except OSError as error:
                messagebox.showerror(
                    "Save Error",
                    str(error)
                )

        

        
    def stop_automated_actions(self):
        """Stop any scheduled autoplay or replay."""

        if self.scheduled_job is not None:
            self.root.after_cancel(self.scheduled_job)
            self.scheduled_job = None

        self.is_autoplaying = False
        self.is_replaying = False



if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()


    
