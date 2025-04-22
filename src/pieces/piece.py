# Định nghĩa các quân cờ
class Piece:
    """
    Khởi tạo một quân cờ với màu và vị trí đầu tiên.
    """
    def __init__(self, color, position):
        self.color = color          # 'red' or 'black"
        self.position = position    # (row, col)
        self.symbol = None          # To be set by subclass
        
    def get_valid_moves(self, board):
        """ (abstract-function)
        Lấy tất cả các nước đi hợp lệ cho quân cờ này. Được triển khai bởi các lớp con
        """
        raise NotImplementedError

    # For debug
    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"