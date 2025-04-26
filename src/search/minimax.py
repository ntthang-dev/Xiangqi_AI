from utils import move_generation
from board.board import Board

class Minimax:
    def search(self, board: Board, depth: int, maximizing_player: bool, ai_color: str):
        """
        Hàm minimax tìm kiếm nước đi tốt nhất không cắt tỉa.
        :param board: trạng thái bàn cờ hiện tại
        :param depth: độ sâu tìm kiếm
        :param maximizing_player: True nếu AI đang đi, False nếu đối thủ đi
        :param ai_color: màu quân của AI ('red' hoặc 'black')
        """
        # Nếu đạt depth 0 hoặc hết game
        if depth == 0 or board.is_game_over():
            score = move_generation.evaluation_board(board, ai_color)
            return None, None, score

        valid_moves = move_generation.get_valid_moves(board, board.current_player)
        flat_moves = move_generation.list1_2list([(piece, [(m, 0) for m in moves]) for piece, moves in valid_moves])

        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None
        best_piece_position = None

        for piece, move, _ in flat_moves:
            board_copy = board.copy()
            from_pos = piece.position
            board_copy.move_piece(from_pos, move)
            # KHÔNG đổi current_player bằng tay! `move_piece` đã tự đổi rồi

            _, _, score = self.search(board_copy, depth - 1, not maximizing_player, ai_color)

            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_piece_position = from_pos
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_piece_position = from_pos

        return best_piece_position, best_move, best_score
