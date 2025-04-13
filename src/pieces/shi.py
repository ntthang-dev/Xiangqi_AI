# Tệp này định nghĩa quân Sĩ (Shi) trong cờ Tướng (Xiangqi).

# Quân Sĩ (仕/士) - Advisor/Guard
from src.pieces.piece import Piece
from src.board.palace import is_in_palace

class Shi(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'S' if color == 'red' else 's'
        
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Advisors can only move diagonally within the palace
        possible_moves = [
            (row+1, col+1), (row+1, col-1),
            (row-1, col+1), (row-1, col-1)
        ]
        
        for move in possible_moves:
            # Check if move is within the palace
            if not is_in_palace(move, self.color):
                continue
            # Check if destination has friendly piece
            piece_at_dest = board.get_piece(move)
            if piece_at_dest and piece_at_dest.color == self.color:
                continue
            
            moves.append(move)
        
        return moves