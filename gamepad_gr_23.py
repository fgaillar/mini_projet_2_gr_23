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

def decode(board):
    """Read the board_str and transform in list

    parameter:
    ------------
    board : the board that is received by the radio

    return:
    ------------
    return board_list (list)
    """
    board_list = [[], [], [], [], []]
    board_str = board.split("-")
    for element, n in zip(board_str, range(100)):
        for e in element:
            board_list[n].append(int(e))
    return board_list

# settings
group_id = 23

# setup radio to receive/send messages
radio.on()
radio.config(group=group_id)

# loop forever (until micro:bit is switched off)
while True:
    # get view of the board
    view = get_message()

    # clear screen
    microbit.display.clear()

    # show view of the board
    board_list = decode(view)
    for x in range(len(board_list)):
        for y in range(len(board_list)):
            if board_list[x][y] == 9:
                microbit.display.set_pixel(x, y, 9)

    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)
    if microbit.button_a.is_pressed():
        # send current direction
        x = microbit.accelerometer.get_x()
        y = microbit.accelerometer.get_y()
        if abs(x) > abs(y):
            if x > 0:
                radio.send('right')
            else:
                radio.send('left')
        elif abs(x) < abs(y):
            if y > 0:
                radio.send('down')
            else:
                radio.send('up')
    elif microbit.button_b.is_pressed():
            # notify that the piece should be dropped
            radio.send('drop')
