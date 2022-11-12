import random

import radio
import microbit


# definition of functions
def get_message():
    """Wait and return a message from another micro:bit.

    Returns
    -------
    message: message sent by another micro:bit (str)

    """

    message = None
    while message == None:
        microbit.sleep(250)
        message = radio.receive()

    return message


def is_collision():
    """Check if the brick is on collision with another or the border

    returns
    ------------
    return True
    """
    for x in range(len(brick)):
        for y in range(len(brick)):
                if board[x][y] > 0 and brick[x][y] > 0:
                    return True
    return False


def execute_order(order, board, brick_x, brick_y):
    piece_dropped = False
    if order == 'drop':
        for row in range(len(brick)):
            for column in range(len(brick[row])):
                if brick[row][column] == 9:
                    board[row + brick_x][column + brick_y] = 9
    else:
        brick_x, brick_y = move(order, brick_x, brick_y)

    return board, brick_x, brick_y, piece_dropped


def move(order, brick_x, brick_y):
    if order == 'left':
        brick_y -= 1
    elif order == 'right':
        brick_y += 1
    elif order == 'down':
        brick_x += 1
    elif order == 'up':
        brick_x -= 1
    return brick_x, brick_y


# settings
group_id = 23

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

bricks = [[9, 9], [9, 0]], [[9, 9], [0, 9]], [[9, 9], [9, 9]], [[9, 9], [0, 0]], [[9, 0], [0, 0]], [[9, 0], [9, 0]], [
    [9, 0], [9, 9]]

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    brick = random.choice(bricks)
    for x in range(2):
        for y in range(2):
            board[x][y] = brick[x][y]

    if is_collision():
        game_is_over = True
    coord_x = 0
    coord_y = 0

    # check if the new piece collide with board
    for x in range(len(brick)):
        for y in range(len(brick)):
            if board[x][y] != 0 and brick != 0:
                game_is_over = True
    if not game_is_over:
        for x in range(len(brick)):
            for y in range(len(brick)):
                board[x][y] = brick[x][y]

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            board_str = ''
            for y in range(len(board)):
                for x in range(len(board)):
                    if board[y][x] > 0:
                        board_str += '9'
                    else:
                        board_str += '0'
                if y != 4:
                    board_str += '-'
            radio.send(board_str)

            # wait until gamepad sends an order
            order = get_message()

            # execute order (drop or move piece)
            if order == "drop":
                board = execute_order(order, board, brick_x, brick_y)
                piece_dropped = True
            else:
                position_brick = execute_order(order, board, brick_x, brick_y)

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
