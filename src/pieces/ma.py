# Tệp này định nghĩa quân Mã (Ngựa) trong cờ Tướng (Xiangqi).
# Quân Mã (马/馬) - Horse/Knight

from pieces.piece import Piece

class Ma(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'M' if color == 'red' else 'm'
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horse moves in an "L" shape: one step orthogonally + one step diagonally outward
        # First check the four orthogonal directions for the first step
        orthogonal_steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for o_step in orthogonal_steps:
            o_row, o_col = row + o_step[0], col + o_step[1]
            
            # Check if the orthogonal step is within the board
            if not (0 <= o_row < 10 and 0 <= o_col < 9):
                continue
            
            # Check if the horse's leg is blocked
            if board.get_piece((o_row, o_col)):
                continue
                
            # Determine the two diagonal moves from this orthogonal position
            if o_step[0] == 0: # Moved horizontally
                diag_steps = [(1, o_step[1]), (-1, o_step[1])]
            else: # Moved vertically
                diag_steps = [(o_step[0], 1), (o_step[0], -1)]
            
            for d_step in diag_steps:
                new_row, new_col = o_row + d_step[0], o_col + d_step[1]
                
                # Check if the move is within board
                if not (0 <= new_row < 10 and 0 <= new_col < 9):
                    continue

                # Check if destination has friendly piece
                piece_at_dest = board.get_piece((new_row, new_col))
                if piece_at_dest and piece_at_dest.color == self.color:
                    continue

                moves.append((new_row, new_col))
            
        return moves