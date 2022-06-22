from pybricks.parameters import Port, Stop, Direction, Button, Color

class Action:
    def __init__(self, left, right, speed, motor3=None):
        self.left = left
        self.right = right
        self.speed = speed
        self.motor3 = motor3

    def act(self):
        ls, rs, s3 = self.speeds()
        self.left.run(ls)
        self.right.run(rs)
        if self.motor3:
            self.motor3.run(s3)

class Forward(Action):
    def speeds(self):
        return self.speed, self.speed, 0

class Backward(Action):
    def speeds(self):
        return -self.speed, -self.speed, 0

class Left(Action):
    def speeds(self):
        return -self.speed, self.speed, 0

class Right(Action):
    def speeds(self):
        return self.speed, -self.speed, 0

class Stop(Action):
    def speeds(self):
        return 0, 0, 0

class SpinClock(Action):
    def speeds(self):
        return 0, 0, self.speed

class SpinCounter(Action):
    def speeds(self):
        return 0, 0, -self.speed

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
