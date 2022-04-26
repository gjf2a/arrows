from pybricks.parameters import Port, Stop, Direction, Button, Color

def drive(ev3, left, right):
    while True:
        pressed = ev3.buttons.pressed()
        if Button.LEFT in pressed:
            left.run(-360)
            right.run(360)
        elif Button.RIGHT in pressed:
            left.run(360)
            right.run(-360)
        elif Button.UP in pressed:
            left.run(360)
            right.run(360)
        elif Button.CENTER in pressed:
            left.stop()
            right.stop()
        elif Button.DOWN in pressed:
            left.run(-360)
            right.run(-360)