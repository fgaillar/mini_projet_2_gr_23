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
    for x in range(len(brick)):
        for y in range(len(brick)):
            if not collision:
                if brick[x][y] > 0 and board[x][y] > 0:
                    collision = True
    return collision

def moove(direction):
    ...

# settings
group_id = 23

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
bricks = [[9, 9], [9, 0]], [[9, 9], [0, 9]], [[9, 9], [9, 9]], [[9, 9], [0, 0]], [[9, 0], [0, 0]], [[9, 0], [9, 0]], []

# loop until game is over
nb_dropped_pieces = 0
game_is_over = False

while not game_is_over:
    # show score (number of pieces dropped)
    microbit.display.show(nb_dropped_pieces)

    # create a new piece in the top left corner
    brick = random.choice(bricks)
    for x in range(len(brick)):
        for y in range(len(brick)):
            microbit.display.set_pixel(x, y, 9)

    # check if the new piece collides with dropped pieces
    is_collision()

    if not game_is_over:
        # ask orders until the current piece is dropped
        piece_dropped = False
        while not piece_dropped:
            # send state of the board to gamepad (as a string)
            board_str = ''
            board_str = board_str.join(board)
            radio.send()

            # wait until gamepad sends an order
            order = get_message()

            # execute order (drop or move piece)
            moove(order)

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
