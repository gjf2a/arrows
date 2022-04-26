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

def buttonLoop(ev3, action_map):
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            action_map[pressed[0]].act()
