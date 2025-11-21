#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import TouchSensor, Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait
from pybricks.media.ev3dev import SoundFile

# EV3-hub og sensorer
ev3 = EV3Brick()
btn = TouchSensor(Port.S3)
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter=49.6, axle_track=105)

color_sensor = ColorSensor(Port.S4)       # Fargesensor
ultra_sensor = UltrasonicSensor(Port.S2)  # Ultrasonisk sensor (brukes ikke ennå)

drive_speed = 75  # mm/s

prosentmaling = [
    (8400,100),(7900,90),(7600,75),(7400,60),
    (7200,45),(7000,30),(6800,18),(6600,10),(6400,0)
]

prosent_lav = 30
prosent_kritisk = 15
cooldown = 60000       # 60 sek
cooldown_lav = 300000  # 5 min
cooldown_ok = 17500    # oppdatering av OK-status
cooldown_farge = 5000  # pausetall 


def mv_til_prosent(mv):
    if mv >= prosentmaling[0][0]: return 100
    elif mv <= prosentmaling[-1][0]: return 0
    for (v_hoy, p_hoy), (v_lav, p_lav) in zip(prosentmaling, prosentmaling[1:]):
        if mv == v_lav: return p_lav
        elif mv == v_hoy: return p_hoy
        elif v_lav < mv < v_hoy:
            t = (mv - v_lav)/(v_hoy - v_lav)
            prosent = p_lav + t * (p_hoy - p_lav)
            return prosent
    return 0

# Tomme metoder for farger
def se_rodt():
    robot.stop()
    wait(5000)
    robot.drive(drive_speed,0)

def se_bla():
    robot.stop()
    ev3.screen.clear()
    ev3.screen.print("Vi er hjemme!")
    ev3.speaker.play_file(SoundFile.DOG_BARK_1)
    wait(2000)

def se_gult():
    robot.stop()
    wait(100)
    robot.turn(110)
    wait(100)

def se_gront():
    robot.stop()
    wait(100)
    robot.turn(-125)
    wait(100)

def passere_hinder():
    robot.stop()
    robot.turn(100)
    robot.drive_time(150, -s40, 5300)   
    robot.stop() 
    robot.turn(125)

tilstand = "OK"
sist_varsel = -cooldown
sist_lav_varsel = -cooldown_lav
sist_ok_varsel = -cooldown_ok
sist_farge_tid = -cooldown_ok
klokke = StopWatch()

# Vent på knapptrykk før start
ev3.screen.print("Trykk på knappen \n"
"for å starte")
while not btn.pressed():
    continue

ev3.light.off()
ev3.screen.clear()
ev3.screen.print("Starter...")

# Hovedløkken
while True:
# Kjør roboten rett frem sakte
    distanse = ultra_sensor.distance()
    if distanse < 100: 
        passere_hinder()
    else: robot.drive(drive_speed,0)

    # Batterimåling
    mv = ev3.battery.voltage()
    prosent = mv_til_prosent(mv)

    # Bestem ny tilstand
    if prosent <= prosent_kritisk:
        tilstand = "Kritisk"
    elif prosent <= prosent_lav:
        tilstand = "Lav"
    else:
        tilstand = "OK"

    # Oppdater lys 
    if tilstand == "Kritisk":
        ev3.light.on(Color.RED)
    elif tilstand == "Lav":
        ev3.light.on(Color.ORANGE)
    else:
        ev3.light.on(Color.GREEN)

    tid = klokke.time()

    # Oppdater skjerm og varsler basert på tilstand og cooldown
    if tilstand == "OK":
        if tid - sist_ok_varsel >= cooldown_ok:
            ev3.screen.clear()
            ev3.screen.print("Batteri \n(~{:.0f}%)".format(prosent))
            sist_ok_varsel = tid

    elif tilstand == "Lav":
        if tid - sist_lav_varsel >= cooldown_lav:
            ev3.speaker.beep(700, 120)
            ev3.screen.clear()
            ev3.screen.print("Batteri lavt \n(~{:.0f}%)".format(prosent))
            sist_lav_varsel = tid

    elif tilstand == "Kritisk":
        if tid - sist_varsel >= cooldown:
            ev3.speaker.beep(900, 120)
            ev3.speaker.beep(900, 120)
            ev3.screen.clear()
            ev3.screen.print("KRITISK batteri! \n(~{:.0f}%)".format(prosent))
            sist_varsel = tid

    # Sjekk farge
    if tid - sist_farge_tid >= cooldown_farge:
        farge = color_sensor.color()
        if farge == Color.RED:
            se_rodt()
            sist_farge_tid = klokke.time()
        elif farge == Color.BLUE:
            se_bla()
            break
        elif farge == Color.YELLOW:
            se_gult()
            sist_farge_tid = tid
        elif farge == Color.GREEN:
            robot.stop()
            se_gront()
            sist_farge_tid = tid

        

