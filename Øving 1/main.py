#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.screen.print("hello world")
wait(500)

# Initialize the drive base.
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor,right_motor, wheel_diameter=49.6, axle_track=118)
robot.straight(100)
robot.turn(90)
robot.straight(300)
robot.turn(90)
robot.straight(100)
robot.turn(90)
robot.straight(300)
robot.turn(90)
ev3.screen.print("Have a nice day!")
wait(2000)
