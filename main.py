#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import driver
import menus
import watcher

ev3 = EV3Brick()

left = Motor(Port.A)
right = Motor(Port.D)

ev3.speaker.beep()

titles = ['drive', 'watch']
functions = [driver.drive, watcher.watch]

choice = menus.menuShowAll(ev3, titles)
print("Choice:", choice)
(functions[choice])(ev3, left, right)
print("Done")