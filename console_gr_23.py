import math
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


def is_collision(brick, board, x, y):
    """Check if the brick is on collision with another or the border
    parameters
    ------------
    brick: brick we want to check (str)
    board: board of the game (str)
    x: coordinate x (int)
    y: coordinate y (int)
    returns
    ------------
    True or False
    """
    if (brick[0][0] > 0 and board[x][y] != 0) or (brick[0][1] > 0 and board[x][y] != 0) or (brick[1][0] > 0 and board[x][y] != 0) or (brick[1][1] > 0 and board[x][y] != 0):
        return True
    else:
        return False


# settings
group_id = 23

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
bricks = [[9, 9], [9, 0]], [[9, 9], [0, 9]], [[9, 9], [9, 9]], [[9, 9], [0, 0]], [[9, 0], [0, 0]]

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    brick = random.choice(bricks)
    microbit.display.set_pixel(0, 0, brick[0][0])
    microbit.display.set_pixel(0, 1, brick[0][1])
    microbit.display.set_pixel(1, 0, brick[1][0])
    microbit.display.set_pixel(1, 1, brick[1][1])

    # check if the new piece collides with dropped pieces
    game_is_over = ...

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(...)

            # wait until gamepad sends an order
            order = get_message()

            # execute order (drop or move piece)
            ...

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
