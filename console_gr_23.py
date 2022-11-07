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


def is_collision():
    """Check if the brick is on collision with another or the border

    returns
    ------------
    True or False
    """
    collision = False
    for x in range(2):
        for y in range(2):
            if not collision:
                if brick[x][y] > 0 and board[x][y] > 0:
                    collision = True
    return collision


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

    # check if the new piece collides with dropped pieces
    is_collision()

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            radio.send(board)

            # wait until gamepad sends an order
            order = get_message()

            # execute order (drop or move piece)
            if order == 'up':
                if not is_collision():
                    for x in range(len(brick)):
                        for y in range(len(brick)):
                            board[x][y] += brick[x-1][y]
            elif order == 'down':
                if not is_collision():
                    for x in range(len(brick)):
                        for y in range(len(brick)):
                            board[x][y] += brick[x+1][y]
            elif order == 'left':
                if not is_collision():
                    for x in range(len(brick)):
                        for y in range(len(brick)):
                            board[x][y] += brick[x][y-1]
            elif order == 'right':
                if not is_collision():
                    for x in range(len(brick)):
                        for y in range(len(brick)):
                            board[x][y] += brick[x][y+1]
            if order == 'drop':
                piece_dropped = True
        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
