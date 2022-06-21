from menus import menuManyOptions
import lib
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port

class SensorTester:
    def __init__(self, sensor, sensor_test, action):
        self.sensor = sensor
        self.sensor_test = sensor_test
        self.action = action

    def act(self):
        if self.sensor_test():
            return self.action

class Controller:
    def __init__(self, default_action, testers):
        self.default_action = default_action
        self.testers = testers

    def control(self):
        while True:
            pressed = ev3.buttons.pressed()
            self.pick_action().act()

    def pick_action(self):
        for tester in self.testers:
            act = tester.act()
            if act:
                return act
        return default_action
            


ports = {'S1': Port.S1, 'S2': Port.S2, 'S3': Port.S3, 'S4': Port.S4}

labels  = ['Default'] + list(ports.keys())
tests   = ['<=', '>']
values  = [['50', '100', '150', '200', '250', '300'], ['0', '1'], ['20', '40', '60', '80'], ['20', '40', '60', '80']]
actions = ['Stop', 'Forward', 'Backward', 'Left', 'Right']

def compare(reading, value, comparator):
    if comparator == '<=':
        return reading <= value
    else:
        return reading > value

sensors = {
    'Sonar': lambda port, test, value, action: SensorTester(UltrasonicSensor(port), lambda s: compare(s.distance(), value, test), action), 
    'Touch': lambda port, test, value, action: SensorTester(TouchSensor(port), lambda s: compare(1 if s.pressed() else 0, value, test), action)
}

speed = 360
actions = {
    'Stop':     lambda left, right: lib.Stop(left, right, 0),
    'Forward':  lambda left, right: lib.Forward(left, right, speed),
    'Backward': lambda left, right: lib.Backward(left, right, speed),
    'Left':     lambda left, right: lib.Left(left, right, speed),
    'Right':    lambda left, right: lib.Right(left, right, speed)
}

def setup(ev3, left, right):
    while True:
        sensor_picks = menuManyOptions(ev3, labels, [list(sensors)] * len(labels))
        comp_picks   = menuManyOptions(ev3, labels, [tests] * len(labels))
        value_picks  = menuManyOptions(ev3, labels, [values] * len(labels))
        action_picks = menuManyOptions(ev3, labels, [list(actions)] * len(labels))

        testers = [sensors[sensor_picks[i]](ports[i], comp_picks[i], value_picks[i], action_picks[i+1](left, right)) for i in range(len(ports))]
        ctrl = Controller(action_picks[0](left, right), testers)
        ctrl.control()