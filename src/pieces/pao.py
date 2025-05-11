
# Tệp này định nghĩa quân Pao (Pháo) trong cờ Tướng (Xiangqi).
from pieces.piece import Piece

class Pao(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'P' if color == 'red' else 'p'
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            jumped = False  # Đã qua 1 quân chắn hay chưa
            jump_count = 0  # Số quân đã nhảy qua

            for i in range(1, 10):
                r, c = row + dr * i, col + dc * i

                if not (0 <= r < 10 and 0 <= c < 9):
                    break  # Thay continue bằng break vì đã ra ngoài bàn cờ

                piece = board.get_piece((r, c))

                if not jumped:
                    if piece is None:
                        moves.append((r, c))
                    else:
                        jumped = True
                        jump_count += 1
                elif piece:
                    if jump_count == 1 and piece.color != self.color:
                        moves.append((r, c))  # Ăn quân sau 1 lần nhảy
                    break
        return moves