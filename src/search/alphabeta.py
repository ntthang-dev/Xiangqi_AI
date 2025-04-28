import time
from utils import move_generation
from board.board import Board
class AlphaBeta:
    def __init__(self):
        self.pruned_branches = 0
        self.time_taken = 0
        self.total_nodes = 0

    def search(self, board: Board, depth: int, is_maximizing: bool, alpha: float, beta: float):
        start_time = time.time()
        self.total_nodes += 1

        ai_color = board.current_player if is_maximizing else ('black' if board.current_player == 'red' else 'red')

        if depth == 0 or board.is_game_over():
            score = move_generation.evaluation_board(board, ai_color)
            self.time_taken += time.time() - start_time
            return None, None, score

        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = None
        best_piece = None

        valid_moves = move_generation.get_valid_moves(board, board.current_player)
        flat_moves = move_generation.list1_2list(valid_moves)
        for piece, move in flat_moves:
            from_pos = piece.position
            captured = board.move_piece(from_pos, move)

            _, _, value = self.search(board, depth - 1, not is_maximizing, alpha, beta)

            board.undo_move(from_pos, move, captured)

            if is_maximizing:
                if value > best_score:
                    best_score = value
                    best_piece = from_pos
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if value < best_score:
                    best_score = value
                    best_piece = from_pos
                    best_move = move
                beta = min(beta, best_score)

            if beta <= alpha:
                self.pruned_branches += 1
                break

        self.time_taken += time.time() - start_time
        return best_piece, best_move, best_score
