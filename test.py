from tictactoe import minimax

EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, "X", EMPTY],
         [EMPTY, EMPTY, EMPTY]]

print(minimax(board))