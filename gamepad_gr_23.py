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


def accelerometer():
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
    board = get_message()
    print(board)

    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)
    while True:
        if microbit.button_a.is_pressed():
            accelerometer()
    while True:
        if microbit.button_b.is_pressed():
            # notify that the piece should be dropped
            radio.send('drop')
