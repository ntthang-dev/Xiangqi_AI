import time
from search.alphabeta import AlphaBeta
def iterative_deepening_search(board, max_depth=5, time_limit=50.0):
    """
    search_engine: là một instance của lớp Minimax hoặc AlphaBeta
    board: trạng thái hiện tại của bàn cờ
    max_depth: độ sâu tối đa cần tìm
    time_limit: thời gian tối đa (tính bằng giây)
    """
    start_time = time.time()
    best_result = None
    alphabeta=AlphaBeta()
    for depth in range(1, max_depth + 1):
        current_time = time.time()
        if current_time - start_time > time_limit:
            print(f"⏱️ Hết thời gian trước depth {depth}, trả kết quả tốt nhất hiện có.")
            break

        print(f"🔍 Đang tìm với độ sâu {depth}...")
        try:

            result = alphabeta.search(board.copy(), depth, is_maximizing=True, alpha=float('-inf'), beta=float('inf'))
            best_result = result
        except Exception as e:
            print(f"❌ Lỗi ở depth {depth}: {e}")
            break

    end_time = time.time()
    print(f"✅ Đã tìm xong đến độ sâu {depth-1}, mất {end_time - start_time:.2f} giây.")

    return best_result  # (best_piece_position, best_move, best_score)
