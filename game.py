#!/home/akshat/miniconda3/envs/machine-learning/bin/python

from formatting import display_board
from ai import is_win, is_loss, is_draw, valid_moves, place_piece, play_move
import numpy as np

BOARD_SIZE = (6, 8)

if __name__ == '__main__':
    board = np.zeros(BOARD_SIZE)
    is_red = False
    display_board(board, is_red)
    while not is_win(board) and not is_loss(board) and not is_draw(board):
        is_red = not is_red
        if is_red:
            valid = False
            column = None
            while not valid:
                print("Pick a column: ", end='')
                column = int(input())
                moves = valid_moves(board)
                if column in moves:
                    valid = True
                else:
                    print("Wrong move, try again!")
            board = place_piece(board, column, player=1)
            display_board(board, is_red)
            board = board * -1
        else:
            print("Thinking...")
            comp_move = play_move(board)
            board = place_piece(board, comp_move, player=1)
            display_board(board, is_red)
            board = board * -1
        if is_win(board) or is_loss(board) or is_draw(board):
            break
    print('GAME OVER')

