"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from shutil import move

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Player X gets first move
    if board == initial_state():
        return X
    
    # Check board to compare number of X's vs O's
    x_counter = 0
    o_counter = 0

    for row in board:
        for letter in row:
            if letter == X:
                x_counter += 1
            elif letter == O:
                o_counter += 1
    
    # Check if X's exceed O's, O turn
    if x_counter > o_counter:
        return O

    # if X's == O's, X turn
    elif o_counter == x_counter:
        return X
    
    elif terminal(board):
        return "Terminal"
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Define an eligibile set
    eligible = set()

    # Check for a terminal board
    if terminal(board):
        return "Terminal"

    # Loop through each row in board searching for EMPTY
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                eligible.add((i, j))
    return eligible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = deepcopy(board)

    # Navigate to the action coordinate
    i = action[0]
    j = action[1]

    # Check for valid action
    if i > 2 or i < 0 or j > 2 or j < 0:
        raise IndexError("Not a valid action")
    elif copy_board[i][j] == X or copy_board[i][j] == O:
        raise IndexError("Not a valid action")

    # Check the turn
    if player(board) == X:
        copy_board[i][j] = X

    elif player(board) == O:
        copy_board[i][j] = O
    
    return copy_board
    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(len(board)):

        # Check if there was a horizontal winner        
        if len(set(board[i])) == 1 and board[i][0] != EMPTY:
            return board[i][0]
        
        # Check if there was a vertical winner
        for j in range(len(board)):
            if i == 0:
                if len(set([board[i][j], board[i+1][j], board[i+2][j]])) == 1 and board[i][j] != EMPTY:
                    return board[i][j]
            elif i == 1:
                if len(set([board[i][j], board[i-1][j], board[i+1][j]])) == 1 and board[i][j] != EMPTY:
                    return board[i][j]
            elif i == 2:
                if len(set([board[i][j], board[i-1][j], board[i-2][j]])) == 1 and board[i][j] != EMPTY:
                    return board[i][j]    

    # Check for a diagnoal winner

    left_diagonal = [board[0][0], board[1][1], board[2][2]]
    right_diagonal = [board[0][2], board[1][1], board[2][0]]

    if len(set(left_diagonal)) == 1 and EMPTY not in left_diagonal:
        return left_diagonal[0]

    elif len(set(right_diagonal)) == 1 and EMPTY not in right_diagonal:
        return right_diagonal[0] 

    return None          

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if the game is over
    if winner(board):
        return True
    if not any(EMPTY in row for row in board):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """


    # Maximizing player picks action that produces highest value

    solutions = {}

    if player(board) == X:

        v = (-1) * math.inf
        optimal_action = None

        # Get all actions
        x_actions = actions(board)

        # Check if terminal
        if x_actions == "Terminal":
            return utility(board)

        # Get the max value for each action
        for action in x_actions:
            value = min_value(result(board, action))
            solutions[action] = value
        
        optimal_action = sorted(solutions.items(), key=lambda x: x[1], reverse=True)[0][0]
            
    elif player(board) == O:

        v = math.inf
        optimal_action = None

        # Get all actions
        o_actions = actions(board)

        # Check if terminal
        if o_actions == "Terminal":
            return utility(board)

        # Get the min value for each action
        for action in o_actions:
            value = max_value(result(board, action))
            solutions[action] = value
        
        optimal_action = sorted(solutions.items(), key=lambda x: x[1])[0][0]
            
    return optimal_action


def max_value(board):
    v = (-1) * (math.inf)

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
     
    return v

def min_value(board):
    v = math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
