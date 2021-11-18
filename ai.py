import numpy as np
from multiprocessing import Pool
from scipy import signal
import math

DEPTH = 6

PROCESS_COUNT = 12

WIN_CONDITIONS = [
    np.ones((4, 1), dtype=int),
    np.ones((1, 4), dtype=int),
    np.eye(4, dtype=int),
    np.fliplr(np.eye(4, dtype=int))
]


class PlayerNode:
    def __init__(self, board):
        self.board = board
        self.player = 1

    def get_children(self, history):
        children = []
        moves = valid_moves(self.board)
        moves = sorted(moves, key=lambda x: -history[x])
        for move in moves:
            new_board = place_piece(self.board, move, player=self.player)
            children.append((EnemyNode(new_board), move))
        return children
    
    def is_terminal(self):
        return is_win(self.board) or is_draw(self.board)

    def is_maximizing_player(self):
        return True


class EnemyNode:
    def __init__(self, board):
        self.board = board
        self.player = -1

    def get_children(self, history):
        children = []
        moves = valid_moves(self.board)
        moves = sorted(moves, key=lambda x: -history[x])
        for move in moves:
            new_board = place_piece(self.board, move, player=self.player)
            children.append((PlayerNode(new_board), move))
        return children

    def is_terminal(self):
        return is_loss(self.board) or is_draw(self.board)

    def is_maximizing_player(self):
        return False


def score_player_board(board):
    convs = [signal.convolve2d(board, cond, mode='valid') for cond in WIN_CONDITIONS]
    flat_convs = np.array([i for conv in convs for row in conv for i in row])
    best = np.max(flat_convs)
    threes = np.sum(flat_convs == 3)
    twos = np.sum(flat_convs == 2)
    score = best + threes/10 + twos/100
    score = min(4, score)
    return score

def score_board(board, depth):
    player_score = score_player_board(board)
    score = player_score - depth/1000
    if is_win(board):
        score = 4
    if is_loss(board):
        score = -4
    return score

def is_loss(board):
    return is_win(board * -1)

def is_win(board):
    convs = [signal.convolve2d(board, cond) for cond in WIN_CONDITIONS]
    result = any([i == 4 for conv in convs for row in conv for i in row])
    return result

def is_draw(board):
    no_win = not is_win(board) and not is_loss(board)
    no_moves = board.size == 0
    return no_win and no_moves

def valid_moves(board):
    result = [idx for idx, value in enumerate(board[0]) if value == 0]
    return np.array(result)

def place_piece(board, column, player=1):
    last_empty_row = np.where(board[:, column] == 0)[0][-1]
    new_board = np.copy(board)
    new_board[last_empty_row, column] = player
    return new_board

def process_node(node):
    score = alpha_beta_pruning(node, DEPTH, -math.inf, math.inf)
    return score

def play_move(board):
    moves = valid_moves(board)
    next_boards = [place_piece(board, move, player=1) for move in moves]
    next_nodes = [EnemyNode(board) for board in next_boards]
    with Pool(PROCESS_COUNT) as p:
        scores = p.map(process_node, next_nodes)
    moves_scores = sorted(zip(moves, scores), key=lambda x: x[1])
    best_move = moves_scores[-1][0]
    return best_move

def alpha_beta_pruning(node, depth, alpha, beta, history=None, max_depth=DEPTH):
    if depth == max_depth:
        history = {move: 0 for move in valid_moves(node.board)}

    if depth == 0 or node.is_terminal():
        return score_board(node.board, depth)

    if node.is_maximizing_player():
        value = -math.inf
        for child, move in node.get_children(history):
            value = max(value, alpha_beta_pruning(child, depth-1, alpha, beta, history))
            alpha = max(alpha, value)
            if alpha >= beta:
                history[move] += 2**depth
                break
        return value
    else:
        value = math.inf
        for child, move in node.get_children(history):
            value = min(value, alpha_beta_pruning(child, depth-1, alpha, beta, history))
            beta = min(beta, value)
            if alpha >= beta:
                history[move] += 2**depth
                break
        return value