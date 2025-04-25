import time
from utils import move_generation
from board.board import Board

class AlphaBeta:
    def __init__(self):
        self.pruned_branches = 0  # Biến để đếm số nhánh bị tỉa
        self.time_taken = 0  # Biến để lưu thời gian chạy

    def search(self, board: Board, depth: int, maximizing_player: bool, alpha: float, beta: float):
        # Bắt đầu đo thời gian
        start_time = time.time()

        # Lấy các nước đi hợp lệ cho người chơi hiện tại
        valid_move = move_generation.get_valid_moves(board, board.current_player)
        valid_move_with_point = move_generation.evaluate_generation(board, valid_move)

        # Nếu đạt độ sâu tối đa hoặc không còn nước đi hợp lệ
        if depth == 0 or not valid_move:
            valid_move_with_point = self.sort_valid_moves(valid_move_with_point, not maximizing_player)  # Sắp xếp các nước đi hợp lệ
            # Tính điểm đánh giá cho các nước đi hợp lệ
            best_move = None
            best_score = float('-inf') if maximizing_player else float('inf')
            best_piece_position = None  # Lưu vị trí quân cờ tốt nhất

            # Duyệt qua các quân cờ và các nước đi hợp lệ để chọn nước đi tốt nhất
            for piece_name, moves in valid_move_with_point:
                for move, score in moves:
                    if maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = move
                            best_piece_position = piece_name.position
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = move
                            best_piece_position = piece_name.position
            # Kết thúc đo thời gian và tính thời gian chạy
            end_time = time.time()
            self.time_taken = end_time - start_time  # Lưu thời gian chạy
            return best_piece_position, best_move, best_score

        best_move = None
        best_score = float('-inf') if maximizing_player else float('inf')
        best_piece_position = None  # Lưu vị trí quân cờ tốt nhất

        # Duyệt qua các quân cờ và các nước đi hợp lệ
        for piece_name, moves in valid_move_with_point:
            for move, score in moves:
                board_copy = board.copy()  # Tạo bản sao của bàn cờ
                board_copy.move_piece(piece_name.position, move)  # Di chuyển quân cờ
                board_copy.current_player = 'black' if board.current_player == 'red' else 'red'  # Chuyển lượt chơi

                # Đệ quy gọi hàm search để tiếp tục tìm kiếm, đồng thời truyền alpha và beta
                _, _, score = self.search(board_copy, depth - 1, not maximizing_player, alpha, beta)

                # Cập nhật giá trị tốt nhất và thực hiện Alpha-Beta pruning
                if maximizing_player:
                    if score > best_score:
                        best_score = score
                        best_move = move
                        best_piece_position = piece_name.position
                    alpha = max(alpha, best_score)  # Cập nhật alpha
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                        best_piece_position = piece_name.position
                    beta = min(beta, best_score)  # Cập nhật beta

                # Nếu có pruning, dừng vòng lặp sớm và tăng đếm số nhánh bị tỉa
                if beta <= alpha:
                    self.pruned_branches += 1  # Tăng số nhánh bị tỉa
                    break

        # Kết thúc đo thời gian và tính thời gian chạy
        end_time = time.time()
        self.time_taken = end_time - start_time  # Lưu thời gian chạy

        return best_piece_position, best_move, best_score

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
