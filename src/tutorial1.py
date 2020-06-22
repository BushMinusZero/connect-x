import copy
import random
import numpy as np


# Gets board at next step if agent drops piece in selected column
def drop_piece(grid, col, piece, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid


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


def agent1(obs, config):

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

    # Otherwise choose randomly
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return random.choice(valid_moves)


def agent2(obs, config):

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
    if okay_two_turn_moves is not None:
        return random.choice(okay_two_turn_moves)

    # Otherwise choose randomly
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return random.choice(valid_moves)
