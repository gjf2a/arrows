from pybricks.parameters import Port, Stop, Direction, Button, Color

class Action:
    def __init__(self, left, right, speed):
        self.left = left
        self.right = right
        self.speed = speed

    def act(self):
        ls, rs = self.speeds()
        self.left.run(ls)
        self.right.run(rs)

class Forward(Action):
    def speeds(self):
        return self.speed, self.speed

class Backward(Action):
    def speeds(self):
        return -self.speed, -self.speed

class Left(Action):
    def speeds(self):
        return -self.speed, self.speed

class Right(Action):
    def speeds(self):
        return self.speed, -self.speed

class Stop(Action):
    def speeds(self):
        return 0, 0

def buttonLoop(ev3, action_map, instructions):
    instructions(ev3)
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if pressed[0] == Button.LEFT_UP:
                return
            ev3.screen.clear()
            instructions(ev3)
            ev3.screen.draw_text(0, 0, str(pressed[0]))
            action_map[pressed[0]].act()

TEXT_HEIGHT = 16
