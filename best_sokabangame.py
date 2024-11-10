import copy

# Constants
WALL = '+'
SPRITE = 'i'
SPRITE_T = 'I'
EMPTY = ' '
TARGET = 'o'
BOX_NS = '!'
BOX_S = '.'
RESTART = ' '
QUIT = 'q'
CONTROLS = "wasd q"

# Test Case 15 Board
TEST_CASE_15_BOARD = [
    [EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL, EMPTY],
    [WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY],
    [WALL, TARGET, SPRITE, BOX_NS, EMPTY, EMPTY, WALL, EMPTY],
    [WALL, WALL, WALL, EMPTY, BOX_NS, TARGET, WALL, EMPTY],
    [WALL, TARGET, WALL, WALL, BOX_NS, EMPTY, WALL, EMPTY],
    [WALL, EMPTY, WALL, EMPTY, TARGET, EMPTY, WALL, WALL],
    [WALL, BOX_NS, EMPTY, BOX_S, BOX_NS, BOX_NS, TARGET, WALL],
    [WALL, EMPTY, EMPTY, EMPTY, TARGET, EMPTY, EMPTY, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]
]

# Helper Functions
def display_board(board):
    """Prints the board."""
    for row in board:
        print(" ".join(row))

def find_sprite(board):
    """Finds the position of the sprite on the board."""
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell in (SPRITE, SPRITE_T):
                return row_idx, col_idx
    return None

def move_sprite(board, direction):
    """Handles sprite movement and interactions."""
    try:
        sprite_pos = find_sprite(board)
        if not sprite_pos:
            return board  # No sprite found, should not happen.

        row, col = sprite_pos
        delta_row, delta_col = {
            "w": (-1, 0),  # Up
            "s": (1, 0),   # Down
            "a": (0, -1),  # Left
            "d": (0, 1)    # Right
        }[direction]

        new_row, new_col = row + delta_row, col + delta_col

        # Interaction Logic
        if board[new_row][new_col] == EMPTY:
            board[new_row][new_col] = SPRITE
            board[row][col] = TARGET if board[row][col] == SPRITE_T else EMPTY

        elif board[new_row][new_col] == TARGET:
            board[new_row][new_col] = SPRITE_T
            board[row][col] = TARGET if board[row][col] == SPRITE_T else EMPTY

        elif board[new_row][new_col] in (BOX_NS, BOX_S):
            # Handle box push
            box_new_row, box_new_col = new_row + delta_row, new_col + delta_col
            if board[box_new_row][box_new_col] in (EMPTY, TARGET):
                board[box_new_row][box_new_col] = BOX_S if board[box_new_row][box_new_col] == TARGET else BOX_NS
                board[new_row][new_col] = SPRITE_T if board[new_row][new_col] == BOX_S else SPRITE
                board[row][col] = TARGET if board[row][col] == SPRITE_T else EMPTY

    except KeyError:
        print("Invalid move. Please use WASD to move, space to restart, or Q to quit.")
    return board

def check_for_win(board):
    """Checks if all targets are covered and no 'I' remains."""
    for row in board:
        if TARGET in row or SPRITE_T in row:
            return False
    return True

# Main Game Loop
original_board = copy.deepcopy(TEST_CASE_15_BOARD)
current_board = copy.deepcopy(TEST_CASE_15_BOARD)

print("Welcome to the game! Use WASD to move, space to restart, and Q to quit.")
display_board(current_board)

while True:
    user_input = input("Your move: ").lower()

    if user_input == QUIT:
        print("Goodbye!")
        break

    elif user_input == RESTART:
        current_board = copy.deepcopy(original_board)
        print("Game restarted.")
    
    elif user_input in CONTROLS:
        current_board = move_sprite(current_board, user_input)

    else:
        print("Invalid move. Please use WASD to move, space to restart, or Q to quit.")
        continue

    display_board(current_board)

    if check_for_win(current_board):
        print("You win!")
        break
