# Tệp này định nghĩa quân Jiang/Shuai (Tướng) trong cờ Tướng (Xiangqi).
from pieces.piece import Piece
from board.palace import is_in_palace
import sys

class JiangShuai(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'J' if color == 'red' else 'j'
        
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # The general can move one step orthogonally (not diagonally)
        possible_moves = [
            (row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)
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

        # Check for "flying general" rule
        # Generals can't face each other in the same column with no pieces between them        
        opposite_color = 'black' if self.color == 'red' else 'red'

        # Scan the column for the opposite general
        start, end = (row + 1, 10) if self.color == 'red' else (row, 0)

        for r in range(start, end, 1 if self.color == 'red' else -1):
            piece = board.get_piece((r, col))
            if piece:
                if piece.__class__.__name__ == 'JiangShuai' and piece.color == opposite_color:
                    # Đối tướng nằm cùng cột và không có quân cản → hợp lệ theo luật "tướng đối mặt"
                    # This is a valid "flying general" attack move
                    moves.append((r, col))
                # There's a piece between generals, so flying general rule doesn't apply
                break 

        return moves