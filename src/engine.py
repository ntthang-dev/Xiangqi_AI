from board.board import Board
from search import alphabeta, minimax
def engine(board: Board,Ai_color:str,type = 'minimax', difficulty = 2):
    """
    This function is the main engine for AI chess game with many types of AI.
    The default setiing is Alpha-beta.
    The default difficulty is 2. (1-3)
        Otherwise, difficulty also set the depth of the search tree."""
    """    if type == 'alpha_beta':
        # Alpha-beta pruning algorithm
        alpha_beta = alphabeta.AlphaBeta()
        best_move = alpha_beta.search(board, depth=difficulty)"""
    if type == 'minimax':
        # Minimax algorithm without pruning
        m = minimax.Minimax()
        maximizing = (board.current_player == Ai_color)
        best_move = m.search(board, depth=difficulty, maximizing_player=maximizing)
    else:
        raise ValueError("Invalid AI type. Use 'alpha_beta' or 'minimax'.")
    
    # The best_move contains the list (From_pos, to_pos)
    print(f"AI move: ", best_move,best_move[0], best_move[1] )
    board.handle_AI_move(best_move[0], best_move[1])