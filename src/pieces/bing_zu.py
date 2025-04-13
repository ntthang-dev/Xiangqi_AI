# Tệp này định nghĩa quân Binh/Tốt (兵/卒) trong cờ Tướng (Xiangqi).
# Quân Tốt/Binh (兵/卒) - Pawn/Soldier

from src.pieces.piece import Piece
from src.board.river import is_across_river

class BingZu(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'B' if color == 'red' else 'b'
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Define direction based on color (red moves up, black moves down)
        direction = 1 if self.color == 'black' else -1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 10:
            piece_at_dest = board.get_piece((new_row, col))
            if not piece_at_dest or piece_at_dest.color != self.color:
                moves.append((new_row, col))
        
        # If the pawn has crossed the river, it can also move horizontally
        if is_across_river(self.position, self.color):
            # Try moving left and right
            for new_col in [col-1, col+1]:
                if 0 <= new_col < 9:
                    piece_at_dest = board.get_piece((row, new_col))
                    if not piece_at_dest or piece_at_dest.color != self.color:
                        moves.append((row, new_col))

        return moves