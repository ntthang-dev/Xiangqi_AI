from utils import move_generation
from board.board import Board
class Minimax:
    def search(self, board: Board, depth: int, maximizing_player: bool):
        valid_move = move_generation.get_valid_moves(board, board.current_player)
        valid_move_with_point = move_generation.evaluate_generation(board, valid_move)
        
        # Nếu đạt độ sâu tối đa hoặc không còn nước đi hợp lệ
        if depth == 0 or not valid_move:
            best_move = None
            best_score = float('-inf') if maximizing_player else float('inf')
            best_piece_position = None  # Lưu vị trí quân cờ tốt nhất
            for piece_name, moves in valid_move_with_point:
                for move, score in moves:
                    if maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = move
                            best_piece_position = piece_name.position  # Lưu vị trí quân cờ tốt nhất
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = move
                            best_piece_position = piece_name.position  # Lưu vị trí quân cờ tốt nhất
            return best_piece_position, best_move, best_score
        
        best_move = None
        best_score = float('-inf') if maximizing_player else float('inf')
        best_piece_position = None  # Lưu vị trí quân cờ tốt nhất
        for piece_name, moves in valid_move_with_point:
            for move, score in moves:
                board_copy = board.copy()  # Tạo bản sao của bàn cờ
                board_copy.move_piece(piece_name.position, move)  # Di chuyển quân cờ
                board_copy.current_player = 'black' if board.current_player == 'red' else 'red'  # Chuyển lượt chơi
                _, _, score = self.search(board_copy, depth - 1, not maximizing_player)  # Đệ quy
                if maximizing_player:
                    if score > best_score:
                        best_score = score
                        best_move = move
                        best_piece_position = piece_name.position  # Lưu vị trí quân cờ tốt nhất
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                        best_piece_position = piece_name.position  # Lưu vị trí quân cờ tốt nhất
                        
        return best_piece_position, best_move, best_score
