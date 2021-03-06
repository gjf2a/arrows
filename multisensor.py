from menus import menuManyOptions, refresh
import lib
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button

ports = {'S1': Port.S1, 'S2': Port.S2, 'S3': Port.S3, 'S4': Port.S4}
port_list = sorted(ports.keys())

act_labels = ['Default'] + port_list
tests      = {'<': lambda x, y: x < y, '>': lambda x, y: x > y, '=': lambda x, y: x == y}

sensors = {
    'None': ([0], ['='], lambda port, test, value, action: SensorTester(None, lambda s: 1, value, test, action)),
    'Sonar': ([i for i in range(100, 1000, 100)], ['<', '>'], lambda port, test, value, action: SensorTester(UltrasonicSensor(port), lambda s: s.distance(), value, test, action)), 
    'Touch': (['closed', 'open'], ['='], lambda port, test, value, action: SensorTester(TouchSensor(port), lambda s: 'closed' if s.pressed() else 'open', value, test, action))
}

sensor_list = sorted(sensors)

speed = 360
actions = {
    'Halt':        lambda left, right, m3: lib.Stop(left, right, 0, m3),
    'Forward':     lambda left, right, m3: lib.Forward(left, right, speed, m3),
    'Backward':    lambda left, right, m3: lib.Backward(left, right, speed, m3),
    'Left':        lambda left, right, m3: lib.Left(left, right, speed, m3),
    'Right':       lambda left, right, m3: lib.Right(left, right, speed, m3),
    'SpinClock':   lambda left, right, m3: lib.SpinClock(left, right, speed, m3),
    'SpinCounter': lambda left, right, m3: lib.SpinCounter(left, right, speed, m3)
}


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
        return self.comparison(self.last_value, self.sensor_target)


class Controller:
    def __init__(self, ev3, default_action, testers, stopper):
        self.ev3 = ev3
        self.default_action = default_action
        self.testers = testers
        self.stopper = stopper
        self.last_values = None

    def control(self):
        while True:
            pressed = self.ev3.buttons.pressed()
            if Button.CENTER in pressed:
                self.stopper.act()
                break
            else:
                self.pick_action().act()

    def pick_action(self):
        values = [s.poll() for s in self.testers]
        passers = [i for i, s in enumerate(self.testers) if s.passes()]
        winner = passers[0] if len(passers) > 0 else len(self.testers)
        value_list = [port_list[i] + ":" + str(values[i]) for i in range(len(values))] + ['Default']
        if value_list != self.last_values:
            refresh(self.ev3, value_list, winner)
            self.last_values = value_list
        return self.testers[winner].action if winner in range(len(self.testers)) else self.default_action


def setup(ev3, left, right):
    action_list = sorted(actions)

    motor3 = menuManyOptions(ev3, ['3rd motor?'], [['No', 'Yes']])
    if motor3[0] == 1:
        motor3 = Motor(Port.B)
    else:
        motor3 = None
        action_list = action_list[:-2]

    sensor_picks = comp_picks = value_picks = action_picks = None
    while True:
        sensor_picks = menuManyOptions(ev3, port_list, [sensor_list] * len(port_list), sensor_picks)
        comp_picks   = menuManyOptions(ev3, port_list, [sensors[sensor_list[s]][1] for s in sensor_picks], comp_picks)
        value_picks  = menuManyOptions(ev3, port_list, [sensors[sensor_list[s]][0] for s in sensor_picks], value_picks)
        action_picks = menuManyOptions(ev3, act_labels, [action_list] * len(act_labels), action_picks)

        testers = []
        for i in range(len(ports)):
            sensor = sensor_list[sensor_picks[i]]
            action = actions[action_list[action_picks[i+1]]](left, right, motor3)
            port = ports[port_list[i]]
            test = tests[sensors[sensor][1][comp_picks[i]]]
            value = sensors[sensor][0][value_picks[i]]
            testers.append(sensors[sensor][2](port, test, value, action))

        default_action = actions[action_list[action_picks[0]]](left, right, motor3)
        ctrl = Controller(ev3, default_action, testers, lib.Stop(left, right, 0, motor3))
        ctrl.control()