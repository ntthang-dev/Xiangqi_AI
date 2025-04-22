# Tệp này định nghĩa quân Tượng (象) trong cờ Tướng (Xiangqi).
from pieces.piece import Piece
from board.river import is_across_river

class Xiang(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'X' if color == 'red' else 'x'
        
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Elephants move exactly 2 steps diagonally
        possible_moves = [
            (row+2, col+2), (row+2, col-2),
            (row-2, col+2), (row-2, col-2)
        ]
        
        for move in possible_moves:
            new_row, new_col = move
            
            # Check if the move is within the board
            if not (0 <= new_row < 10 and 0 <= new_col < 9):
                continue
            
            # Elephants can't cross the river
            if is_across_river(move, self.color):
                continue
            
            # Check the "elephant eye" (point in between the start and end positions)
            eye_row = (row + new_row) // 2
            eye_col = (col + new_col) // 2
            
            if board.get_piece((eye_row, eye_col)):
                # Eye is blocked
                continue
            
            # Check if destination has friendly piece
            piece_at_dest = board.get_piece(move)
            if piece_at_dest and piece_at_dest.color == self.color:
                continue

            moves.append(move)
        
        return moves