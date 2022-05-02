from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib

def watch(ev3, left, right):
    ev3.screen.clear()
    sonar = UltrasonicSensor(Port.S4)
    last = 0
    while True:
        current = sonar.distance()
        if current != last:
            ev3.screen.draw_box(0, 0, ev3.screen.width, lib.TEXT_HEIGHT, fill=True, color=Color.WHITE)
            ev3.screen.draw_text(0, 0, current)
            last = current