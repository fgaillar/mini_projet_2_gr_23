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


..........
..........
..........

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
    ..........

    # wait for button A or B to be pressed
    while not (microbit.button_a.is_pressed() or microbit.button_b.is_pressed()):
        microbit.sleep(50)

    if microbit.button_a.is_pressed():
        # send current direction
        ..........
        ..........
        ..........

        radio.send(..........)
    elif microbit.button_b.is_pressed():
        # notify that the piece should be dropped
        radio.send(..........)