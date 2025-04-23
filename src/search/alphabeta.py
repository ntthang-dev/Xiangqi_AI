from utils import move_generation
class AlphaBeta:
    def evaluate(self, board):
        """
        Kết hợp đánh giá theo:
        - Zili (子力): Giá trị vật chất
        - Shizhan (势战): Thế trận
        - Kongjian (空间): Kiểm soát không gian
        """
        valid_moves = move_generation.get_valid_moves(board, board.current_color)
        return self.material_eval(board) * 0.6 + self.positional_eval(board) * 0.4
    