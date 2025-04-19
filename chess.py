import tkinter as tk
import chess
import random

# Chess AI (Improved)
class ChessAI:
    def __init__(self, board):
        self.board = board

    def get_best_move(self):
        return self.minimax(self.board, 2, -float('inf'), float('inf'), True)['move']  # Reduced depth for faster AI response

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return {'score': self.evaluate_board(board)}

        legal_moves = list(board.legal_moves)
        if maximizing_player:
            max_eval = -float('inf')
            best_move = None
            legal_moves.sort(key=lambda move: self.evaluate_move(board, move), reverse=True)
            for move in legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth-1, alpha, beta, False)['score']
                board.pop()
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return {'score': max_eval, 'move': best_move}
        else:
            min_eval = float('inf')
            best_move = None
            legal_moves.sort(key=lambda move: self.evaluate_move(board, move), reverse=False)
            for move in legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth-1, alpha, beta, True)['score']
                board.pop()
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return {'score': min_eval, 'move': best_move}

    def evaluate_board(self, board):
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 1000
        }

        score = 0
        for square in range(64):
            piece = board.piece_at(square)
            if piece:
                piece_value = piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score += piece_value
                else:
                    score -= piece_value
        
        score += self.evaluate_mobility(board)
        score += self.evaluate_center_control(board)
        score += self.evaluate_king_safety(board)
        score += self.evaluate_pawn_structure(board)
        
        return score

    def evaluate_move(self, board, move):
        board.push(move)
        score = self.evaluate_board(board)
        board.pop()
        return score

    def evaluate_mobility(self, board):
        white_mobility = len([move for move in board.legal_moves if board.turn == chess.WHITE])
        black_mobility = len([move for move in board.legal_moves if board.turn == chess.BLACK])
        return (white_mobility - black_mobility) * 0.1

    def evaluate_center_control(self, board):
        center_squares = [27, 28, 35, 36]
        score = 0
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += 0.2
                else:
                    score -= 0.2
        return score

    def evaluate_king_safety(self, board):
        score = 0
        for square in range(64):
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.KING:
                king_square = square
                row, col = divmod(king_square, 8)
                for r in range(max(0, row-1), min(7, row+1)+1):
                    for c in range(max(0, col-1), min(7, col+1)+1):
                        if board.piece_at(r*8 + c) and board.piece_at(r*8 + c).color == piece.color:
                            score += 0.1
        return score

    def evaluate_pawn_structure(self, board):
        score = 0
        for square in range(8, 56, 8):
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    score += 0.1
                else:
                    score -= 0.1
        return score

# Chess GUI (Board)
class ChessGUI:
    def __init__(self, root):
        self.board = chess.Board()
        self.ai = ChessAI(self.board)
        self.selected_square = None
        self.valid_moves = []
        self.square_buttons = {}
        
        self.root = root
        self.root.title("Chess Game")
        
        self.setup_board()
        self.update_gui()
    
    def setup_board(self):
        for row in range(8):
            for col in range(8):
                square = (row, col)
                button = tk.Button(self.root, width=6, height=3, command=lambda sq=square: self.on_square_click(sq))
                button.grid(row=row, column=col)
                self.square_buttons[square] = button

    def on_square_click(self, square):
        if self.selected_square:
            self.move_piece(self.selected_square, square)
            self.selected_square = None
        else:
            self.selected_square = square
            self.highlight_valid_moves(square)
    
    def highlight_valid_moves(self, square):
        self.valid_moves = []
        piece = self.board.piece_at(self.get_square_index(square))
        if piece:
            self.valid_moves = [move for move in self.board.legal_moves if move.from_square == self.get_square_index(square)]
        
        # Remove any highlights after a move is made
        for move in self.valid_moves:
            row, col = divmod(move.to_square, 8)
            self.square_buttons[(row, col)].config(bg='lime green')

    def move_piece(self, from_square, to_square):
        from_index = self.get_square_index(from_square)
        to_index = self.get_square_index(to_square)
        
        move = chess.Move(from_index, to_index)
        
        if move in self.board.legal_moves:
            self.board.push(move)
            self.update_gui()
            self.ai_move()
    
    def ai_move(self):
        ai_move = self.ai.get_best_move()
        self.board.push(ai_move)
        self.update_gui()
    
    def update_gui(self):
        for square, button in self.square_buttons.items():
            row, col = square
            piece = self.board.piece_at(self.get_square_index((row, col)))
            if piece:
                piece_symbol = str(piece).upper() if piece.color == chess.WHITE else str(piece).lower()
                button.config(text=piece_symbol)
            else:
                button.config(text="")
        
        # Clear the highlights
        for square, button in self.square_buttons.items():
            button.config(bg='SystemButtonFace')
        
        if self.board.is_game_over():
            self.show_game_over_message()

    def show_game_over_message(self):
        if self.board.is_checkmate():
            message = "Checkmate! AI wins!" if self.board.turn == chess.WHITE else "Checkmate! You win!"
        elif self.board.is_stalemate():
            message = "Stalemate! It's a draw."
        elif self.board.is_insufficient_material():
            message = "Insufficient material! It's a draw."
        elif self.board.is_seventyfive_moves():
            message = "Draw due to 75-move rule."
        elif self.board.is_variant_draw():
            message = "Draw due to variant rule."
        else:
            message = "Game over."
        
        self.show_message(message)
    
    def show_message(self, message):
        message_label = tk.Label(self.root, text=message, font=('Arial', 14))
        message_label.grid(row=8, columnspan=8)

    def get_square_index(self, square):
        row, col = square
        return row * 8 + col

# Start Game
def start_game():
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_game()
