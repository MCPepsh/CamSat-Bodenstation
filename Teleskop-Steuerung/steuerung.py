import json
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
    return math.atan2(x, y)

def hoeheWinkel(geo1, h1, geo2, h2):
    a = abs(h1 - h2)
    b = geoDist(geo1, geo2)
    return math.atan2(a, b)

def toDeg(x):
    return (x / math.pi) * 180

def toRad(x):
    return (x / 180) * math.pi

ended = False
with open("settings.json", 'r') as settings:
    settings = json.load(settings)
    loc = settings["location"]
    lok = settings["lookingAt"]
    hig = settings["height"]
    drehW = geoWinkel(loc, lok)
    #drehW = settings["drehWinkel"]

    teleAusrichtung = drehW
    schwW = math.atan((1000 - hig) / geoDist(loc, lok))
    schwW = hoeheWinkel(loc, hig, lok, 0)
    schwW = settings["schwenkWinkel"]

    print(drehW)
    print(schwW)
    print(str(toDeg(drehW)) + '°')
    print(str(toDeg(schwW)) + '°')


maxDrehGeschw = toRad(1.5)
maxSchwGeschw = toRad(1.5)
drehG = 0
schwG = 0
#datenOut = serial.Serial("COM4", 115200)
#sleep(3)


starttime = time()
#while(not ended):
for i in range(60):
    with open("../Visualisierung/Visualisierung/aktuelledaten.txt", 'r') as daten:
        daten = daten.readlines()
        if(not len(daten) == 0):
            daten[0] = re.sub("\n", "", daten[0])
            daten[0] = re.split(",", daten[0])
            daten[1] = re.split(",", daten[1])
            akt_pos = [float(daten[1][0]), float(daten[1][1])]
            akt_hig = float(daten[1][2])
            #print(daten)
            #print(akt_pos)
            #print(akt_hig)

            drehR = geoWinkel(akt_pos, loc)
            schwR = hoeheWinkel(loc, hig, akt_pos, akt_hig)
            relDrehR = drehR - drehW
            relSchwR = schwR - schwW
            print(toDeg(relDrehR))
            print(toDeg(relSchwR))
            drehG = limitSpeed(relDrehR)

            schwG = limitSpeed(relSchwR)

            drehW = limit(drehW + drehG, teleAusrichtung - math.pi / 2, teleAusrichtung + math.pi / 2)
            drehGOut = (toDeg(drehG) / 1.5) * 500
            drehGOut = ("x" + str(drehGOut)).encode()
            schwGOut = (toDeg(schwG) / 1.5) * 500
            schwGOut = ("y" + str(schwGOut)).encode()
            print(drehGOut)
            #datenOut.write(drehGOut)
            print(schwGOut)
            #datenOut.write(schwGOut)
    sleep(0.5 - ((time() - starttime) % 0.5))
    print("\n")
datenOut.close()
