import sys
import os
from board.board import Board
import copy
from evaluation.shi_zhi import ShiZhi
def get_chess_of_color(color: str) -> list:
    """
    Get the chess pieces of a specific color.
    
    :param color: The color of the chess pieces ('red' or 'black').
    :return: A list of chess pieces of the specified color.
    """
    if color == 'red':
        return ['R','M','X','S','J','P','B']
    elif color == 'black':
        return ['r','m','x','s','j','p','b']
    else:
        raise ValueError("Invalid color. Use 'red' or 'black'.")
def get_valid_moves(board: Board, AI_color: str) -> list:
    board_map = board.board
    valid_move = []
    AI_chess = get_chess_of_color(AI_color)
    
    # Bước 1: Lấy tất cả nước đi hợp lệ ban đầu
    for i in board_map:
        for j in i:
            if j is None:
                continue
            if j.symbol in AI_chess:
                raw_moves = j.get_valid_moves(board)
                filtered_moves = []
                for move in raw_moves:
                    if is_move_legal(board, j, move):
                        filtered_moves.append(move)
                if filtered_moves:
                    valid_move.append((j, filtered_moves))
    
    # Bước 2: Kiểm tra lặp cho từng quân
    final_moves = []
    for piece, moves in valid_move:
        is_piece_repeating = False
        for move in moves:
            temp_board = board.copy()
            temp_board.move_piece(piece.position, move)
            temp_board.current_player = AI_color  
            if temp_board.is_repeating_state(color=AI_color, repeat_limit=3):
                is_piece_repeating = True
                print("Repeating Detected!!!")
                break

        if not is_piece_repeating:
            final_moves.append((piece, moves))  # Giữ quân này lại

    # Nếu lọc xong mà không còn nước nào, quay lại dùng valid_move ban đầu
    return final_moves

def evaluate_generation(board: Board, valid_moves: list) -> list:
    """
    Generate evaluation scores for each possible move,
    using the same logic as evaluation_board().
    """
    result = []
    evaluating_color = board.current_player  # Lấy màu hiện tại đang đi

    for piece, moves in valid_moves:
        move_scores = []
        for move in moves:
            board_copy = board.copy()
            board_copy.move_piece(piece.position, move)
            board_copy.current_player = evaluating_color  # Reset lại màu để đánh giá chuẩn

            shizhi = checkShizhi(board_copy, evaluating_color)
            shizhan = checkShizhan(board_copy, evaluating_color)
            kongjian = checkKongjian(board_copy, evaluating_color)

            total_score = shizhi + shizhan + kongjian
            move_scores.append((move, total_score))

        result.append((piece, move_scores))
    return result

def list1_2list(valid_move:list)->list:

    """
    This func convert the list from (piece,[(move1,value),(move2,value),...]) to [(piece,move1,value1),(piece,move2,value2),...]
    """
    result = []
    for piece, moves in valid_move:
        for move, value in moves:
            result.append((piece, move, value))
    return result

def evaluation_board(board: Board, evaluating_color: str) -> int:
    """
    Đánh giá trạng thái bàn cờ theo hướng của evaluating_color (AI).
    """
    opponent = 'black' if evaluating_color == 'red' else 'red'
    if board.is_checkmate(evaluating_color):
        return -99999999
    if board.is_checkmate(opponent):
        return 99999999

    return (
        checkShizhi(board, evaluating_color)
        + checkShizhan(board, evaluating_color)
        + checkKongjian(board, evaluating_color)
    )

def checkShizhi(board: Board, evaluating_color: str) -> int:
    AI_chess = get_chess_of_color(evaluating_color)
    piece_value = ShiZhi()
    value_AI, value_Opp = 0, 0

    for row in board.board:
        for piece in row:
            if piece is None:
                continue
            if piece.symbol in AI_chess:
                value_AI += piece_value.get_value(piece)
            else:
                value_Opp += piece_value.get_value(piece)

    return value_AI - value_Opp

def checkShizhan(board: Board, evaluating_color: str) -> int:
    score = 0
    for row in board.board:
        for piece in row:
            if piece and piece.color == evaluating_color:
                r, _ = piece.position
                if piece.__class__.__name__.lower() in ['ma', 'ju', 'pao']:
                    if (evaluating_color == 'red' and r < 5) or (evaluating_color == 'black' and r > 4):
                        score += 5
    return score

def checkKongjian(board: Board, evaluating_color: str) -> int:
    total_valid_moves_AI = 0
    total_valid_moves_opp = 0
    AI_chess = get_chess_of_color(evaluating_color)

    for row in board.board:
        for piece in row:
            if piece is None:
                continue
            moves = piece.get_valid_moves(board)
            if piece.symbol in AI_chess:
                total_valid_moves_AI += len(moves)
            else:
                total_valid_moves_opp += len(moves)

    return (total_valid_moves_AI - total_valid_moves_opp) * 100
def is_move_legal(board: Board, piece, move) -> bool:
    """Check if a move is legal (does not leave own king in check)"""
    original_pos = piece.position
    captured_piece = board.get_piece(move)
    
    # Make the move
    board.board[original_pos[0]][original_pos[1]] = None
    board.board[move[0]][move[1]] = piece
    piece.position = move

    # Check if in check
    in_check = board.is_in_check(piece.color)

    # Undo move
    board.board[original_pos[0]][original_pos[1]] = piece
    piece.position = original_pos
    board.board[move[0]][move[1]] = captured_piece
    return not in_check
