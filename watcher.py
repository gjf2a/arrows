from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

def watch(ev3, left, right):
    sonar = UltrasonicSensor(Port.S4)
    while True:
        ev3.screen.print(sonar.distance())