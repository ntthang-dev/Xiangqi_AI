# Tệp này định nghĩa quân Ju (Xe) trong cờ Tướng (Xiangqi).
# Quân Xe (车/車) - Chariot/Rook

from src.pieces.piece import Piece

class Ju(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "R" if color == 'red' else 'r'
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Chariots move any distance orthogonally (like rooks in chess)
        # Check in all four directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for d_row, d_col in directions:
            for i in range(1, 10): # Max possible steps
                new_row, new_col = row + d_row * i, col + d_col * i
                
                # Check if the move is within the board
                if not (0 <= new_row < 10 and 0 <= new_col < 9):
                    break
                
                # Check if there's a piece at the destination
                piece_at_dest = board.get_piece((new_row, new_col))
                
                if not piece_at_dest:
                    # Empty square, valid move
                    moves.append((new_row, new_col))
                else:
                    # Found a piece
                    if piece_at_dest.color != self.color:
                        # Enemy piece, can capture
                        moves.append((new_row, new_col))
                    # Stop in this direction regardless of piece color
                    break
        return moves