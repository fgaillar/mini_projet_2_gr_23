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


def move(direction, coord_x, coord_y):
    """move the brick through the board
    parameter:
    ---------------
    direction: direction th brick will move (str)
    coord_x: coordinates x of the brick (int)
    coord_y: coordinates y of the brick (int)

    return:
    ---------------

    """
    if direction == 'up':
        coord_x -= 1
        if board[coord_x][coord_y]:
            if board[coord_x][coord_y] == 0:
                board[coord_x][coord_y] = brick[coord_x][coord_y]
    if direction == 'down':
        coord_x += 1
        if board[coord_x][coord_y]:
            if board[coord_x][coord_y] == 0:
                board[coord_x][coord_y] = brick[coord_x][coord_y]
    if direction == 'left':
        coord_y -= 1
        if board[coord_x][coord_y]:
            if board[coord_x][coord_y] == 0:
                board[coord_x][coord_y] = brick[coord_x][coord_y]
    if direction == 'right':
        coord_y += 1
        if board[coord_x][coord_y]:
            if board[coord_x][coord_y] == 0:
                board[coord_x][coord_y] = brick[coord_x][coord_y]
    return coord_x, coord_y


# settings
group_id = 23

# setup radio to receive orders
radio.on()
radio.config(group=group_id)

# create empty board + available pieces
board = [[0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]

bricks = [[9,9],[9,0]],[[9,9],[0,9]],[[9,9],[9,9]],[[9,9],[0,0]],[[9,0],[0,0]],[[9,0],[9,0]],[[9,0],[9,9]]

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
            move(order, coord_x, coord_y)
            if order == 'drop':
                piece_dropped = True
                nb_dropped_pieces += 1
            else:
                coord_x, coord_y = move(order, coord_x, coord_y)

        # wait a few milliseconds and clear screen
        microbit.sleep(500)
        microbit.display.clear()

# tell that the game is over
microbit.display.scroll('Game is over', delay=100)
