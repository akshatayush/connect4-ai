def red(string):
    return f"\033[91m {string} \033[00m"

def blue(string):
    return f"\033[94m {string} \033[00m"

def grey(string):
    return f"\033[90m {string} \033[00m"

ICONS = {1: red("O"), 0: grey("."), -1: blue("O")}

def display_board(board, is_red):
    print(' ' + '   '.join([str(i) for i in range(len(board[0]))]))
    sign = 1 if is_red else -1
    print('\n'.join([' '.join([ICONS[item*sign] for item in row]) for row in board]))
    print('-'*30)