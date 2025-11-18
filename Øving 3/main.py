#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
import time
import random
from pybricks.media.ev3dev import SoundFile

# --- Oppsett ---
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
line_sensor = ColorSensor(Port.S3)
sonic_sensor = UltrasonicSensor(Port.S2)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# --- Linjefølging parametere ---
BLACK = 9
WHITE = 90
threshold = (BLACK + WHITE) / 2
DRIVE_SPEED = 100
PROPORTIONAL_GAIN = 1.5


# --- Underholdningsfunksjoner ---

def vits():
    ev3.speaker.say("Hvorfor går roboten til legen?")
    wait(1000)
    ev3.speaker.say("Fordi den hadde fått et virus!")
    ev3.speaker.say("Ha ha ha!")
    wait(1000)

def heart():
    heart1 = [
        "  * *  ",
        " ***** ",
        "  ***  ",
        "   *   "
    ]
    ev3.screen.clear()
    for line in heart1:
        ev3.screen.print(line)
    wait(3000)

def sang():
    ev3.speaker.beep(frequency=262, duration=500)  # C4
    ev3.speaker.beep(frequency=262, duration=500)
    ev3.speaker.beep(frequency=262, duration=500)
    ev3.speaker.beep(frequency=330, duration=500)  # E4
    ev3.speaker.beep(frequency=294, duration=500)  # D4
    ev3.speaker.beep(frequency=294, duration=500)
    ev3.speaker.beep(frequency=294, duration=500)
    ev3.speaker.beep(frequency=349, duration=500)  # F4
    ev3.speaker.beep(frequency=330, duration=500)
    ev3.speaker.beep(frequency=330, duration=500)
    ev3.speaker.beep(frequency=294, duration=500)
    ev3.speaker.beep(frequency=294, duration=500)
    ev3.speaker.beep(frequency=262, duration=500)
    wait(1000)

def vits2():
    ev3.speaker.say("Hvordan vet du at en robot er dårlig på smalltalk?")
    wait(1000)
    ev3.speaker.say("Den svarer bare med null eller én!")
    ev3.speaker.say("Ha ha ha!")
    wait(1000)

# --- Tidsstyring for underholdning ---
last_time = time.time()
pause_numbers = 0
MAX_PAUSES = 10

# stopp


# --- Hovedløkke ---
while True:
    # --- Linjefølging ---
    deviation = line_sensor.reflection() - threshold
    avstand = sonic_sensor.distance()
    if avstand < 100:
        robot.stop()
        ev3.speaker.play_file(SoundFile.CHEERING)
        break
        
        
    elif deviation < 0:
        turn_rate = PROPORTIONAL_GAIN * deviation / 3.5
    else:
        turn_rate = PROPORTIONAL_GAIN * deviation

    robot.drive(DRIVE_SPEED, turn_rate)

    # --- Underholdning hver 10. sekund, maks 10 ganger ---
    current_time = time.time()
    if (current_time - last_time >= 10) and (pause_numbers < MAX_PAUSES):
        robot.stop()  # Stopper for underholdning
        ev3.screen.clear()
        ev3.screen.print("Pause nr.", pause_numbers + 1)

        tall = random.randint(1, 4)
        if tall == 1:
            heart()
        elif tall == 2:
            vits()
        elif tall == 3:
            sang()
        else:
            vits2()

        pause_numbers += 1
        last_time = time.time()

    wait(10)  # Litt delay for å ikke overbelaste CPU-en
