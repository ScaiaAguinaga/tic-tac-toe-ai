from GameStatus_5120 import GameStatus

# Returns next best move using minimax algorithm with alpha-beta pruning
# Best move varies based on the depth chosen
def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()

    if (depth == 0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None
    
    
    # If maximizing player look for max, otherwise look for min
    if maximizingPlayer:
        max_eval = float('-inf')
        best_move = None
        # Create a new state with each possible move and recursively call minimax
        for move in game_state.get_moves():
            new_state = game_state.get_new_state(move)
            eval, _ = minimax(new_state, depth - 1, False, alpha, beta)
            # Update best move with its score
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            # Alpha-beta pruning
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        # Create a new state with each possible move and recursively call minimax
        for move in game_state.get_moves():
            new_state = game_state.get_new_state(move)
            eval, _ = minimax(new_state, depth - 1, True, alpha, beta)
            # Update best move with its score
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            # Alpha-beta pruning
            if beta <= alpha:
                break
        return min_eval, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None

    max_eval = float('-inf')
    best_move = None
    # Create a new state with each possible move and recursively call negamax
    for move in game_status.get_moves():
        new_state = game_status.get_new_state(move)
        eval, _ = negamax(new_state, depth - 1, -turn_multiplier, -beta, -alpha)
        eval = -eval
        # Update best move with its score
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
        # Alpha-beta pruning
        if alpha >= beta:
            break
    return max_eval, best_move