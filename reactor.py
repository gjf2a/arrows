from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib
from menus import menuManyOptions

# These values are in millimeters. 
# 150 was barely enough to dodge the wall. We need some further-out ones. Keep one of 50 or 100 for the
# collision experience.
cutoffs = ['50', '100', '150']

def react(ev3, left, right):
    choices = menuManyOptions(ev3, ['Cutoff'], [cutoffs])
    cutoff = int(cutoffs[choices[0]])
    under = lib.Left(left, right, 360)
    over = lib.Forward(left, right, 360)
    sonar = UltrasonicSensor(Port.S4)
    last = 0
    while True:
        current = sonar.distance()
        if current != last:
            ev3.screen.draw_box(0, 0, ev3.screen.width, lib.TEXT_HEIGHT * 2, fill=True, color=Color.WHITE)
            ev3.screen.draw_text(0, 0, current)
            last = current
            if current < cutoff:
                under.act()
                message = "Under "
            else:
                over.act()
                message = "Over "
            ev3.screen.draw_text(0, lib.TEXT_HEIGHT, message + str(cutoff))