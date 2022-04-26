from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib

def drive(ev3, left, right):
    action_map = {
        Button.LEFT:   lib.Left(left, right, 360),
        Button.RIGHT:  lib.Right(left, right, 360),
        Button.UP:     lib.Forward(left, right, 360),
        Button.DOWN:   lib.Backward(left, right, 360),
        Button.CENTER: lib.Stop(left, right, 360)
    }

    ev3.screen.clear()
    for i, s in enumerate(["UP -> Forward", 'LEFT -> Turn left', 'RIGHT -> Turn right', 'DOWN -> Backward', 'CENTER -> Stop', 'UP_LEFT -> Quit']):
        ev3.screen.draw_text(0, i * lib.TEXT_HEIGHT, s)
    lib.buttonLoop(ev3, action_map)