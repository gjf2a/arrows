from menus import menuManyOptions, refresh
import lib
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button

ports = {'S1': Port.S1, 'S2': Port.S2, 'S3': Port.S3, 'S4': Port.S4}
port_list = sorted(ports.keys())

act_labels = ['Default'] + port_list
tests      = ['<=', '>']

sensors = {
    'None': ([0], lambda port, test, value, action: SensorTester(None, lambda s: 1, value, test, action)),
    'Sonar': ([i for i in range(50, 350, 50)], lambda port, test, value, action: SensorTester(UltrasonicSensor(port), lambda s: s.distance(), value, test, action)), 
    'Touch': ([0, 1], lambda port, test, value, action: SensorTester(TouchSensor(port), lambda s: 1 if s.pressed() else 0, value, test, action))
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


class SensorTester:
    def __init__(self, sensor, sensor_getter, sensor_target, comparison, action):
        self.sensor = sensor
        self.sensor_getter = sensor_getter
        self.sensor_target = sensor_target
        self.comparison = comparison
        self.action = action
        self.last_value = None

    def poll(self):
        self.last_value = self.sensor_getter(self.sensor)
        return self.last_value

    def passes(self):
        return compare(self.last_value, self.sensor_target, self.comparison)


class Controller:
    def __init__(self, ev3, default_action, testers):
        self.ev3 = ev3
        self.default_action = default_action
        self.testers = testers

    def control(self):
        while True:
            pressed = self.ev3.buttons.pressed()
            if Button.CENTER in pressed:
                break
            else:
                self.pick_action().act()

    def pick_action(self):
        values = [s.poll() for s in self.testers]
        passers = [(i, s.passes()) for i, s in enumerate(self.testers)]
        winner = passers[0][0] if len(passers) > 0 else len(passers)
        value_list = [port_list[i] + ":" + str(values[i]) for i in range(len(values))] + ['Default']
        refresh(self.ev3, value_list, winner)
        return self.testers[winner].action if winner in range(len(self.testers)) else default_action


def compare(reading, value, comparator):
    if comparator == '<=':
        return reading <= value
    else:
        return reading > value


def setup(ev3, left, right):
    while True:
        sensor_picks = menuManyOptions(ev3, port_list, [sensor_list] * len(port_list))
        comp_picks   = menuManyOptions(ev3, port_list, [tests] * len(port_list))
        value_picks  = menuManyOptions(ev3, port_list, [sensors[sensor_list[s]][0] for s in sensor_picks])
        action_picks = menuManyOptions(ev3, act_labels, [action_list] * len(act_labels))

        testers = []
        for i in range(len(ports)):
            sensor = sensor_list[sensor_picks[i]]
            action = actions[action_list[action_picks[i+1]]](left, right)
            testers.append(sensors[sensor][1](ports[port_list[i]], comp_picks[i], value_picks[i], action))

        ctrl = Controller(ev3, actions[action_list[action_picks[0]]](left, right), testers)
        ctrl.control()