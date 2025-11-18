#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.B) 
right_motor = Motor(Port.A) 
left_sensor = ColorSensor(Port.S1) 
right_sensor = ColorSensor(Port.S2) 
robot = DriveBase(left_motor, right_motor, wheel_diameter=81.6, axle_track=104) 

# Write your program here.
Black = 11
White = 100
threshold = (Black + White) / 2 #vurder å dele opp for hver sensor

while True:
    error = (right_sensor.reflection() - threshold) - (left_sensor.reflection() - threshold) #svinger venstre når høyre sensor ser for mye hvit. hold langs venstre siden av linjen
    Kp = 0.95 #konstant som bestemmer hvor mye turn rate skal bli
    turn = Kp * error
    robot.drive(285 , turn)

wait(5)
