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
        if self.sensor_test(self.sensor):
            return self.action

class Controller:
    def __init__(self, ev3, default_action, testers):
        self.ev3 = ev3
        self.default_action = default_action
        self.testers = testers

    def control(self):
        while True:
            pressed = self.ev3.buttons.pressed()
            self.pick_action().act()

    def pick_action(self):
        for tester in self.testers:
            act = tester.act()
            if act:
                return act
        return default_action
            


ports = {'S1': Port.S1, 'S2': Port.S2, 'S3': Port.S3, 'S4': Port.S4}
port_list = sorted(ports.keys())

act_labels = ['Default'] + port_list
tests      = ['<=', '>']
#values     = [['50', '100', '150', '200', '250', '300'], ['0', '1'], ['20', '40', '60', '80'], ['20', '40', '60', '80']]
#actions    = ['Stop', 'Forward', 'Backward', 'Left', 'Right']

def compare(reading, value, comparator):
    if comparator == '<=':
        return reading <= value
    else:
        return reading > value

sensors = {
    'None': ([0], lambda port, test, value, action: SensorTester(None, lambda s: False, action)),
    'Sonar': ([50, 100, 150, 200, 250, 300], lambda port, test, value, action: SensorTester(UltrasonicSensor(port), lambda s: compare(s.distance(), value, test), action)), 
    'Touch': ([0, 1], lambda port, test, value, action: SensorTester(TouchSensor(port), lambda s: compare(1 if s.pressed() else 0, value, test), action))
}

sensor_list = sorted(sensors)

speed = 360
actions = {
    'Stop':     lambda left, right: lib.Stop(left, right, 0),
    'Forward':  lambda left, right: lib.Forward(left, right, speed),
    'Backward': lambda left, right: lib.Backward(left, right, speed),
    'Left':     lambda left, right: lib.Left(left, right, speed),
    'Right':    lambda left, right: lib.Right(left, right, speed)
}

action_list = sorted(actions)

def setup(ev3, left, right):
    while True:
        sensor_picks = menuManyOptions(ev3, port_list, [sensor_list] * len(port_list))
        comp_picks   = menuManyOptions(ev3, port_list, [tests] * len(port_list))
        value_picks  = menuManyOptions(ev3, port_list, [sensors[sensor_list[s]][0] for s in sensor_picks])
        action_picks = menuManyOptions(ev3, act_labels, [action_list] * len(act_labels))

        testers = []
        for i in range(len(ports)):
            sensor = sensor_list[sensor_picks[i]]
            print(i, sensor)
            print(ports[port_list[i]], comp_picks[i], value_picks[i])
            print(action_picks[i+1])
            print(actions[action_list[action_picks[i+1]]](left, right))
            testers.append(sensors[sensor][1](ports[port_list[i]], comp_picks[i], value_picks[i], actions[action_list[action_picks[i+1]]](left, right)))

        #testers = [sensors[sensor_list[sensor_picks[i]]](ports[i], comp_picks[i], value_picks[i], action_picks[i+1](left, right)) for i in range(len(ports))]
        ctrl = Controller(ev3, actions[action_list[action_picks[0]]](left, right), testers)
        ctrl.control()