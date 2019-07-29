import json
from turtle import *
import math
from time import *
import re
import serial
import struct
import random


def winkel(p1, p2):
    return math.atan2(float(p1[1]) - float(p2[1]), float(p1[0]) - float(p2[0])) - math.atan2(0, 1)

def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

def limitSpeed(n):
    return limit(n, -maxDrehGeschw, maxDrehGeschw)

def geoDist(a, b):
    p1 = [toRad(a[0]), toRad(a[1])]
    p2 = [toRad(b[0]), toRad(b[1])]
    return 6372795.477598 * math.acos(math.sin(p1[0]) * math.sin(p2[0]) + math.cos(p1[0]) * math.cos(p2[0]) * math.cos(p1[1]-p2[1]))

def geoWinkel(a, b):
    p1 = [toRad(a[0]), toRad(a[1])]
    p2 = [toRad(b[0]), toRad(b[1])]
    x = math.cos(p2[0]) * math.sin(p2[1] - p1[1])
    y = math.cos(p1[0]) * math.sin(p2[0]) - math.sin(p1[0]) * math.cos(p2[0]) * math.cos(p2[1] - p1[1])
    #print("x: " + str(x))
    #print("y: " + str(y))
    return math.atan2(x, y)

def toDeg(x):
    return (x / math.pi) * 180

def toRad(x):
    return (x / 180) * math.pi

ended = False
with open("settings.json", 'r') as settings:
    settings = json.load(settings)
    loc = settings["location"]
    #drehWinkel = settings["angle"]
    lok = settings["lookingAt"]
    hig = settings["height"]
    drehWinkel = geoWinkel(loc, lok)

    teleAusrichtung = drehWinkel
    schwenkW = math.atan((1000 - hig) / dist(loc, lok))
    #print(loc)
    #print(str(toDeg(geoWinkel([39.099912, -94.581213], [38.627089, -90.200203]))) + "°")
    #print(str(toDeg(drehWinkel)) + "°")
    #print(str(toDeg(schwenkW)) + "°")
    #print(1000 - hig)
    #print(geoDist(loc, lok))
    #print(loc)
    #print(lok)
    #print(lok)

maxDrehGeschw = toRad(1.5)
geschw = 0
#datenOut = serial.Serial("COM4", 115200)
sleep(3)

'''speed(0)
ht()
#left(90)
goto(0, 0)
color("black")
#clear()
goto(0, 400)
goto(0, 0)
right(toDeg(drehWinkel))
forward(400)
backward(400)
left(toDeg(drehWinkel))
clear()'''

starttime = time()
#while(not ended):
for i in range(60):
    with open("../CamSatVisuallisierung001/Visualisierung/aktuelledaten.txt", 'r') as daten:
        daten = daten.readlines()
        if(not len(daten) == 0):
            #daten = daten.readlines()
            daten[0] = re.sub("\n", "", daten[0])
            daten[0] = re.split(",", daten[0])
            daten[1] = re.split(",", daten[1])
            akt_pos = [float(daten[1][0]), float(daten[1][1])]
            height = float(daten[1][2])
            print("\n")
            print(daten)
            print(akt_pos)
            print(height)
            #print(loc)

            x_richtung = winkel(daten[1], loc)
            rel_x_richtung = x_richtung - drehWinkel
            #print(str(richtung) + "°    " + str(rel_richtung) + "°")
            #print(str(geoDist(loc, akt_pos) / 1000) + " km")
            #print(str(360 - toDeg(geoWinkel(loc, akt_pos))) + "°")
            #print(str(toDeg(geoWinkel(loc, akt_pos))) + "°")
            x_geschw = limitSpeed(rel_x_richtung)

            y_geschw = limitSpeed(toRad(-5))

            drehWinkel = limit(drehWinkel + x_geschw, teleAusrichtung - math.pi / 2, teleAusrichtung + math.pi / 2)
            #print(str(toDeg(drehWinkel)) + "°")
            #geschw = 0.01500009999999999848819490190265 / 3333.3111112592586075637316782082
            #geschwout = int((float("x" + str(toDeg(x_geschw)).encode("utf-8")) / 1.5) * 500)
            #x_geschwout = ("x" + str(toDeg(x_geschw))).encode("utf-8")
            x_geschwout = (toDeg(x_geschw) / 1.5) * 500
            x_geschwout = ("x" + str(x_geschwout)).encode()
            y_geschwout = (toDeg(y_geschw) / 1.5) * 500
            y_geschwout = ("y" + str(y_geschwout)).encode()
            #geschwout = "1".encode("utf-8")
            #geschwout = b'123'
            #geschwout = random.random()
            #geschwout = b'16'
            #geschwout = bytes(str(geschwout).encode("utf-8"))
            #geschwout = b'123.45'
            print(x_geschwout)
            #datenOut.write(x_geschwout)
            print(y_geschwout)
            #datenOut.write(y_geschwout)


            
            #color("black")
            '''clear()
            up()
            goto(0, 400)
            down()
            goto(0, 0)
            right(drehWinkel)
            forward(400)
            backward(400)
            left(drehWinkel)
            up()
            goto(0, 0)
            down()
            right(richtung)
            color("red")
            forward(400)
            left(richtung)
            up()
            goto(0, 0)
            down()
            right(rel_richtung)
            color("blue")
            forward(400)
            left(rel_richtung)'''
            '''clear()
            width(0)
            up()
            goto(0, 0)
            down()
            goto(0, 1000)
            goto(0, -1000)
            width(2)
            up()
            goto(0, -1)
            down()
            color("red")
            forward(rel_richtung * 100)
            up()
            goto(0, 1)
            down()
            color("blue")
            forward(geschw * 100)'''
            '''clear()
            up()
            goto(0, 0)
            down()
            #goto(10, 0)
            #goto(-10, 0)

            up()
            goto(250, -300)
            down()
            left(90)
            circle(250, 180)

            up()
            goto(250, -300)
            left(180)
            circle(250, 90 + toDeg(richtung))
            down()
            color("red")
            width(10)
            forward(0)
            color("black")
            width(0)
            up()
            circle(250, 90 - toDeg(richtung))

            goto(250, -300)
            left(180)
            circle(250, 90 + toDeg(drehWinkel))
            down()
            color("blue")
            width(5)
            forward(0)
            color("black")
            width(0)
            up()
            circle(250, 90 - toDeg(drehWinkel))
            
            down()

            right(270)

            up()
            goto(0, 300)
            down()
            left(180)
            circle(250, 90)
            left(180)

            up()
            goto(0, 300)
            left(90)
            circle(250, 30)
            down()
            color("red")
            width(10)
            forward(0)
            color("black")
            width(0)
            up()
            circle(250, 90 - 30)

            goto(0, 300)
            right(90)
            circle(250, 60)
            down()
            color("blue")
            width(5)
            forward(0)
            color("black")
            width(0)
            up()
            circle(250, 90 - 60)
            
            left(90)'''
    sleep(0.5 - ((time() - starttime) % 0.5))
datenOut.close()
