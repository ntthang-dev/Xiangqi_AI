
from pieces.piece import Piece
class ShiZhi:
    PIECE_VALUE = {
        'jiang': 0,  # Tướng phải được bảo vệ
        'pao': 400,      # Pháo giá trị thay đổi theo thế trận
        'ju':1000,      # Xe
        'ma': 450,       # Ngựa giá trị thay đổi theo thế trận
        'xiang': 250,    # Tượng
        'shi': 200,      # Sĩ
        'bing_0': 100,  # Binh chưa qua sông
        'bing_1': 200,  # Binh đã qua sông
    }
    SYMBOL_MAP = {
        'j': 'jiang',
        'p': 'pao',
        'r': 'ju',
        'm': 'ma',
        'x': 'xiang',
        's': 'shi'
    }
    def get_value(self, piece):
        symbol = piece.symbol.lower()
        if symbol == 'b':
            row = piece.position[0]
            if (piece.color == 'red' and row < 5) or (piece.color == 'black' and row > 4):
                return self.PIECE_VALUE['bing_0']
            else:
                return self.PIECE_VALUE['bing_1']
        else:
            piece_name = self.SYMBOL_MAP.get(symbol)
            return self.PIECE_VALUE.get(piece_name, 0)
