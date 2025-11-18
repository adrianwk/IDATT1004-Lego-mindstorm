#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

# Create your objects here.
ev3 = EV3Brick()
ts = TouchSensor(Port.S1)
us = UltrasonicSensor(Port.S2)

vinkel = random.randint(100,140)
retning = 1
sving = vinkel * retning
tall = random.randint(-1,1)
while tall == 0:
    tall = random.randint(-1,1)


# Write your program here.
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
robot = DriveBase(left_motor,right_motor, wheel_diameter=49.6, axle_track=118)

running = False 

while True:
    if ts.pressed():
        running = not running
        wait(500)
        if running:
            ev3.speaker.say("Exercise 2")
        else:
            robot.stop()
            ev3.speaker.say("Exercise done")     
            break  

    if running:
        avstand=us.distance()
        if avstand < 75:
            vinkel = random.randint(100,140)
            sving = vinkel * retning
            robot.stop()
            robot.straight(-30)
            robot.turn(sving)
            tall = random.randint(-1,1)
            while tall == 0:
                tall = random.randint(-1,1)
            retning = retning * tall

        else:
            robot.drive(200, 0)
    



