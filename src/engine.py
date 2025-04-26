from board.board import Board
from search import alphabeta, minimax, iterative_deepening
def engine(board: Board,Ai_color:str,type = 'minimax', difficulty = 2):
    """
    This function is the main engine for AI chess game with many types of AI.
    The default setiing is Alpha-beta.
    The default difficulty is 2. (1-3)
        Otherwise, difficulty also set the depth of the search tree."""
    if type == 'alpha_beta':
        # Alpha-beta pruning algorithm
        alpha_beta = alphabeta.AlphaBeta()
        best_move = alpha_beta.search(board, depth=difficulty,is_maximizing=(board.current_player == Ai_color), alpha=float('-inf'), beta=float('inf'))
        print(f"Total nodes searched: {alpha_beta.total_nodes}")
        print(f"Number of pruned branches: {alpha_beta.pruned_branches}")
        print(f"Time taken for search: {alpha_beta.time_taken:.4f} seconds")
    elif type == 'minimax':
        # Minimax algorithm without pruning
        m = minimax.Minimax()
        maximizing = (board.current_player == Ai_color)
        best_move = m.search(board, depth=difficulty, maximizing_player=maximizing)
    elif type == 'iterative_deepening':
        # Iterative deepening search algorithm
        best_move = iterative_deepening.iterative_deepening_search(board, max_depth=difficulty, time_limit=50.0)
        print(best_move)
    else:
        raise ValueError("Invalid AI type. Use 'alpha_beta' or 'minimax'.")
    
    # The best_move contains the list (From_pos, to_pos)
    print(f"AI move: ", best_move,best_move[0], best_move[1] )
    board.handle_AI_move(best_move[0], best_move[1])