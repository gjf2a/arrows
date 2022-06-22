#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import driver, menus, watcher, reactor, multisensor

ev3 = EV3Brick()

left = Motor(Port.A)
right = Motor(Port.D)

ev3.speaker.beep()

titles = ['Motor Demo', 'Sonar Demo', 'Reactive']#, 'Sonar Reaction']
functions = [driver.drive, watcher.watch, multisensor.setup]#, reactor.react]

choice = menus.menuShowAll(ev3, titles)
(functions[choice])(ev3, left, right)