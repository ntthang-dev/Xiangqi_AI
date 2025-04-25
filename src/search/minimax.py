from utils import move_generation
from board.board import Board
class Minimax:
    def search(self, board: Board, depth: int, maximizing_player: bool):
        # Nếu đạt lá hoặc không còn nước đi → trả về evaluation
        if depth == 0 or board.is_game_over():
            score = move_generation.evaluation_board(board)
            return None, None, score

        # Lấy tất cả nước đi hợp lệ và chuyển về dạng [(piece, move, _)]
        valid_moves = move_generation.get_valid_moves(board, board.current_player)
        flat_moves = move_generation.list1_2list([(piece, [(m, 0) for m in moves]) for piece, moves in valid_moves])  # bỏ điểm vì không cần

        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None
        best_piece_position = None

        for piece, move, _ in flat_moves:
            board_copy = board.copy()
            board_copy.move_piece(piece.position, move)
            board_copy.current_player = 'black' if board.current_player == 'red' else 'red'

            _, _, score = self.search(board_copy, depth - 1, not maximizing_player)

            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_piece_position = piece.position
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_piece_position = piece.position

        return best_piece_position, best_move, best_score
