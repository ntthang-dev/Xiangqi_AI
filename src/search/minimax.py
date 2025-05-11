import time
from utils import move_generation
from board.board import Board

class Minimax:
    def __init__(self):
        self.time_taken = 0
        self.total_nodes = 0
    def search(self, board: Board, depth: int, is_maximizing: bool):
        """
        Hàm minimax tìm kiếm nước đi tốt nhất không cắt tỉa.
        :param board: trạng thái bàn cờ hiện tại
        :param depth: độ sâu tìm kiếm
        :param maximizing_player: True nếu AI đang đi, False nếu đối thủ đi
        :param ai_color: màu quân của AI ('red' hoặc 'black')
        """
        start_time = time.time()
        self.total_nodes += 1
        ai_color = board.current_player if is_maximizing else ('black' if board.current_player == 'red' else 'red')
        # Nếu đạt depth 0 hoặc hết game
        if depth == 0 or board.is_game_over():
            score = move_generation.evaluation_board(board, ai_color)
            return None, None, score

        valid_moves = move_generation.get_valid_moves(board, board.current_player)
        flat_moves = move_generation.list1_2list(valid_moves )

        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = None
        best_piece = None

        for piece, move in flat_moves:
            from_pos = piece.position
            captured = board.move_piece(from_pos, move)

            _, _, value = self.search(board, depth - 1, not is_maximizing)

            board.undo_move(from_pos, move, captured)

            if is_maximizing:
                if value > best_score:
                    best_score = value
                    best_piece = from_pos
                    best_move = move
            else:
                if value < best_score:
                    best_score = value
                    best_piece = from_pos
                    best_move = move
        self.time_taken += time.time() - start_time
        return best_piece, best_move, best_score
