import time
from utils import move_generation
from board.board import Board

class AlphaBeta:
    def __init__(self):
        self.pruned_branches = 0  # Biến để đếm số nhánh bị tỉa
        self.time_taken = 0  # Biến để lưu thời gian chạy


    def search(self, board: Board, depth: int, is_maximizing: bool, alpha: float, beta: float):
        start_time = time.time()

        if depth == 0 or board.is_game_over():
            score = move_generation.evaluation_board(board)
            return None, None, score


        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = None
        best_piece = None

        valid_moves = move_generation.get_valid_moves(board, board.current_player)
        valid_moves_with_scores = move_generation.evaluate_generation(board, valid_moves)
        sorted_moves = self.sort_valid_moves(valid_moves_with_scores, is_maximizing)
        flat_moves = move_generation.list1_2list(sorted_moves)

        for piece, move, _ in flat_moves:
            board_copy = board.copy()
            board_copy.move_piece(piece.position, move)
            board_copy.current_player = 'black' if board.current_player == 'red' else 'red'

            _, _, value = self.search(board_copy, depth - 1, not is_maximizing, alpha, beta)

            if is_maximizing:
                if value > best_score:
                    best_score = value
                    best_move = move
                    best_piece = piece.position
                alpha = max(alpha, best_score)
            else:
                if value < best_score:
                    best_score = value
                    best_move = move
                    best_piece = piece.position
                beta = min(beta, best_score)

            if beta <= alpha:
                self.pruned_branches += 1
                break

        self.time_taken += time.time() - start_time
        return best_piece, best_move, best_score

    def sort_valid_moves(self, valid_moves, maximizing_player):
        """
        Sort the list of [piece, [(move, score), ...]] by the best move score of each piece.

        If maximizing: sort by highest score of a piece's moves.
        If minimizing: sort by lowest score of a piece's moves.
        """
        def best_score(moves):
            # Kiểm tra xem moves có rỗng không trước khi sử dụng min hoặc max
            if not moves:
                return float('-inf') if maximizing_player else float('inf')  # Trả về giá trị cực đại/cực tiểu nếu không có nước đi

            if maximizing_player:
                return max(score for _, score in moves)
            else:
                return min(score for _, score in moves)

        valid_moves.sort(key=lambda x: best_score(x[1]), reverse=maximizing_player)
        return valid_moves
