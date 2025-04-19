import tkinter as tk
import chess
import chess.engine
import threading
import time
import random

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess with AI")

        self.board = chess.Board()
        self.buttons = {}
        self.selected_square = None
        self.valid_moves = []
        self.highlighted = []

        self.square_colors = [("white", "lightblue"), ("black", "lightgreen")]
        self.square_size = 60

        self.create_board()
        self.update_gui()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                button = tk.Button(
                    self.root,
                    width=6,
                    height=3,
                    command=lambda sq=square: self.on_square_click(sq),
                    font=("Arial", 16, "bold")
                )
                button.grid(row=row, column=col)
                self.buttons[square] = button

    def update_gui(self):
        for square, button in self.buttons.items():
            piece = self.board.piece_at(square)
            button.config(text=piece.symbol() if piece else "", fg="yellow" if piece and piece.color else "lightblue")

            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            color_index = (row + col) % 2
            button.config(bg=self.square_colors[color_index][0])

        for square in self.highlighted:
            self.buttons[square].config(bg="lime")

        for square in self.valid_moves:
            self.buttons[square].config(text="●", fg="lime")

    def on_square_click(self, square):
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.valid_moves = [move.to_square for move in self.board.legal_moves if move.from_square == square]
                self.highlighted = [square]
                self.update_gui()
        else:
            if square in self.valid_moves:
                move = chess.Move(self.selected_square, square)
                if self.is_pawn_promotion(move):
                    promo = self.ask_promotion()
                    if promo:
                        move.promotion = promo
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.selected_square = None
                    self.valid_moves = []
                    self.highlighted = []
                    self.update_gui()

                    if self.board.is_game_over():
                        self.show_result()
                        return

                    threading.Thread(target=self.make_ai_move).start()
            else:
                self.selected_square = None
                self.valid_moves = []
                self.highlighted = []
                self.update_gui()

    def is_pawn_promotion(self, move):
        piece = self.board.piece_at(move.from_square)
        return piece and piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]

    def ask_promotion(self):
        promo_win = tk.Toplevel(self.root)
        promo_win.title("Promote Pawn")
        promo_win.grab_set()

        chosen = tk.StringVar()

        def select_piece(piece_type):
            chosen.set(piece_type)
            promo_win.destroy()

        tk.Label(promo_win, text="Promote to:", font=("Arial", 12, "bold")).pack(pady=5)

        pieces = [("Queen", chess.QUEEN), ("Rook", chess.ROOK), ("Bishop", chess.BISHOP), ("Knight", chess.KNIGHT)]
        for name, val in pieces:
            tk.Button(promo_win, text=name, width=10, command=lambda v=val: select_piece(v)).pack(pady=2)

        self.root.wait_window(promo_win)
        return int(chosen.get()) if chosen.get() else None

    def make_ai_move(self):
        time.sleep(1.5)
        best_move = self.get_best_ai_move()
        if best_move:
            self.board.push(best_move)
            self.highlighted = [best_move.from_square, best_move.to_square]
            self.update_gui()
            if self.board.is_game_over():
                self.show_result()

    def get_best_ai_move(self):
        best_score = -float("inf")
        best_move = None

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.evaluate_board()
            self.board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate_board(self):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        return score

    def show_result(self):
        result = self.board.result()
        msg = ""
        if result == "1-0":
            msg = "You win! 🎉"
        elif result == "0-1":
            msg = "You lost. 💀 Skill issue."
        else:
            msg = "Draw. Try again."

        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        tk.Label(popup, text=msg, font=("Arial", 16, "bold")).pack(padx=20, pady=20)
        tk.Button(popup, text="Exit", command=self.root.quit, font=("Arial", 12)).pack(pady=10)

def start_game():
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()

start_game()
