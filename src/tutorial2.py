import copy
import random
import numpy as np


# Returns True if dropping piece in column results in game win
def check_winning_move(obs, config, col, piece):
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    next_grid = drop_piece(grid, col, piece, config)
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[row, col:col+config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(next_grid[row:row+config.inarow, col])
            if window.count(piece) == config.inarow:
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    return False


# Calculates score if agent drops piece in selected column
def score_move(grid, col, mark, config):
    next_grid = drop_piece(grid, col, mark, config)
    score = get_heuristic(next_grid, mark, config)
    return score


# Helper function for score_move: gets board at next step if agent drops piece in selected column
def drop_piece(grid, col, mark, config):
    next_grid = grid.copy()
    for row in range(config.rows - 1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid


# Helper function for score_move: calculates value of heuristic for grid
def get_heuristic(grid, mark, config):
    A = 1000000
    B = 100
    C = 10
    D = -5
    E = -1000

    num_twos = count_windows(grid, 2, mark, config)
    num_threes = count_windows(grid, 3, mark, config)
    num_fours = count_windows(grid, 4, mark, config)
    num_twos_opp = count_windows(grid, 2, mark % 2 + 1, config)
    num_threes_opp = count_windows(grid, 3, mark % 2 + 1, config)
    score = A * num_fours + B * num_threes + C * num_twos + D * num_twos_opp + E * num_threes_opp
    return score


# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs, piece, config):
    return (window.count(piece) == num_discs and window.count(0) == config.inarow - num_discs)


# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[row, col:col + config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns):
            window = list(grid[row:row + config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[range(row, row + config.inarow), range(col, col + config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow - 1, config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows


def avoid_two_turn_loss(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)

    moves = []
    for move in valid_moves:
        next_grid = drop_piece(grid, move, 1, config)
        next_board = next_grid.reshape(1, config.rows * config.columns).tolist()[0]
        next_obs = copy.deepcopy(obs)
        next_obs.board = next_board
        opponent_can_win = check_if_there_is_a_winning_move(next_obs, config, 2)
        if not opponent_can_win:
            moves.append(move)
    return moves


def check_if_there_is_a_winning_move(obs, config, piece):
    agent_wins_next_move = [check_winning_move(obs, config, c, piece)
                            for c in range(config.columns) if obs.board[c] == 0]
    if any(agent_wins_next_move):
        return agent_wins_next_move.index(True)


# The agent is always implemented as a Python function that accepts two arguments: obs and config
def agent3(obs, config):
    # Get list of valid moves
    valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    # Use the heuristic to assign a score to each possible board in the next turn
    scores = dict(zip(valid_moves, [score_move(grid, col, obs.mark, config) for col in valid_moves]))
    # Get a list of columns (moves) that maximize the heuristic
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    # Select at random from the maximizing columns
    return random.choice(max_cols)


# The agent is always implemented as a Python function that accepts two arguments: obs and config
def agent4(obs, config):
    # First check if the agent can win, if so, then do it
    agent_wins_next_move = [(c, check_winning_move(obs, config, c, 1))
                            for c in range(config.columns) if obs.board[c] == 0]
    indices, booleans = zip(*agent_wins_next_move)
    if any(booleans):
        return indices[booleans.index(True)]

    # Next, check if the opponent can win, if so, then block them
    opponent_wins_next_move = [(c, check_winning_move(obs, config, c, 2))
                               for c in range(config.columns) if obs.board[c] == 0]
    indices, booleans = zip(*opponent_wins_next_move)
    if any(booleans):
        return indices[booleans.index(True)]

    # Next, avoid moves that cause your opponent to win
    okay_two_turn_moves = avoid_two_turn_loss(obs, config)

    # Get list of valid moves
    valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    # Use the heuristic to assign a score to each possible board in the next turn
    scores = dict(zip(valid_moves, [score_move(grid, col, obs.mark, config) for col in valid_moves]))
    # Get a list of columns (moves) that maximize the heuristic
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]

    # Select at random from the maximizing columns
    okay_two_turn_moves = [] if okay_two_turn_moves is None else okay_two_turn_moves
    okay_scores = {k: v for k, v in scores.items() if k in okay_two_turn_moves}
    max_two_turn_moves = [key for key in okay_scores.keys() if okay_scores[key] == max(okay_scores.values())]
    if max_two_turn_moves:
        return random.choice(max_two_turn_moves)
    else:
        return random.choice(max_cols)
