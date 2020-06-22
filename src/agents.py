import random


from kaggle_environments import evaluate
import numpy as np
from tutorial1 import agent1, agent2
from tutorial2 import agent3, agent4


# Selects random valid column
def agent_random(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return random.choice(valid_moves)


# Selects middle column
def agent_middle(obs, config):
    return config.columns//2


# Selects leftmost valid column
def agent_leftmost(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return valid_moves[0]


# To learn more about the evaluate() function, check out the documentation here: (insert link here)
def get_win_percentages(a1, a2, n_rounds=100):
    # Use default Connect Four setup
    config = {'rows': 6, 'columns': 7, 'inarow': 4}
    # Agent 1 goes first (roughly) half the time
    outcomes = evaluate("connectx", [a1, a2], config, [], n_rounds//2)
    # Agent 2 goes first (roughly) half the time
    outcomes += [[b, a] for [a, b] in evaluate("connectx", [a2, a1], config, [], n_rounds-n_rounds//2)]
    print("Agent 1 Win Percentage:", np.round(outcomes.count([1, -1])/len(outcomes), 2))
    print("Agent 2 Win Percentage:", np.round(outcomes.count([-1, 1])/len(outcomes), 2))
    print("Number of Invalid Plays by Agent 1:", outcomes.count([None, 0]))
    print("Number of Invalid Plays by Agent 2:", outcomes.count([0, None]))
    print("Number of Draws (in {} game rounds):".format(n_rounds), outcomes.count([0, 0]))


def main():
    get_win_percentages(a1=agent4, a2=agent3)


if __name__ == '__main__':
    main()
