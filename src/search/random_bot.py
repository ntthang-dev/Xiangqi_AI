import random
from board.board import Board

def random_bot_move(board: Board):
    legal_moves = board.get_legal_moves(board.current_player)
    if not legal_moves:
        return False  # Bot hết nước đi

    move = random.choice(legal_moves)
    from_pos, to_pos = move
    board.handle_AI_move(from_pos, to_pos)
    return True
