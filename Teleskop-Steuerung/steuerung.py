import json
import math
from turtle import *
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

def limitSpeed(n, maxG):
    return limit(n, -maxG, maxG)

def geoDist(a, b):      # https://www.sunearthtools.com/en/tools/distance.php#txtDist_1
    p1 = [toRad(a[0]), toRad(a[1])]
    p2 = [toRad(b[0]), toRad(b[1])]
    return 6372795.477598 * math.acos(math.sin(p1[0]) * math.sin(p2[0]) + math.cos(p1[0]) * math.cos(p2[0]) * math.cos(p1[1]-p2[1]))

def geoWinkel2(a, b):
    p1 = [toRad(a[0]), toRad(a[1])]
    p2 = [toRad(b[0]), toRad(b[1])]
    x = math.cos(p2[0]) * math.sin(p2[1] - p1[1])
    y = math.cos(p1[0]) * math.sin(p2[0]) - math.sin(p1[0]) * math.cos(p2[0]) * math.cos(p2[1] - p1[1])
    return math.atan2(y, x)

def geoWinkel(a, b):    # https://www.sunearthtools.com/en/tools/distance.php#txtDist_3
    latA = toRad(a[0])
    lonA = toRad(a[1])
    latB = toRad(b[0])
    lonB = toRad(b[1])
    delta_phi = math.log(math.tan(latB / 2 + math.pi / 4) / math.tan(latA / 2 + math.pi / 4))
    delta_lon = abs(lonA - lonB)
    if(delta_lon > toRad(180)):
        delta_lon = delta_lon(mod(toRad(180)))
    theta = math.atan2(delta_lon, delta_phi)
    #print("delta_phi: " + str(delta_phi))
    #print("delta_lon: " + str(delta_lon))
    #print(theta)
    return(theta)

def hoeheWinkel(geo1, h1, geo2, h2):
    a = abs(h1 - h2)
    b = geoDist(geo1, geo2)
    return math.atan2(a, b)

def toDeg(x):
    return (x / math.pi) * 180

def toRad(x):
    return (x / 180) * math.pi

ended = False

#print("winkel: " + str(toDeg(geoWinkel([51.86, 7.7], [51.96, 7.8]))) + '°')

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

##    left(90)
##    width(5)
##    ht()
####    forward(0)
####    up()
####    goto((lok[1] - loc[1]) * 1000, (lok[0] - loc[0]) * 1000)
####    down()
####    forward(0)
####    up()
####    goto(0, 0)
##    color('red')
##    width(3)
##    down()
##    right(toDeg(drehW))
##    forward(dist(loc, lok) * 1000)
    print(drehW)
    print(schwW)
    print(str(toDeg(drehW)) + '°')
    print(str(toDeg(schwW)) + '°')

interval = 1/5          # 1/5 geht noch gut
maxDrehG = toRad(3 * interval)
maxSchwG = toRad(3 * interval)
maxDrehG = toRad(0.3 * interval)
maxSchwG = toRad(0.3 * interval)
print(interval)
drehG = 0
schwG = 0
datenOut = serial.Serial("COM4", 115200)
sleep(3)


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

            drehR = geoWinkel(loc, akt_pos)
            schwR = hoeheWinkel(loc, hig, akt_pos, akt_hig)
            relDrehR = drehR - drehW
            relSchwR = schwR - schwW
            #print("relDrehR: " + str(toDeg(relDrehR)) + '°')
            #print("relSchwR: " + str(toDeg(relSchwR)) + '°')
            #print("Drehrichtung: " + str(toDeg(drehR)) + '°')
            #print("Drehwinkel:   " + str(toDeg(drehW)) + '°')
            #print("Teleausricht: " + str(toDeg(teleAusrichtung)) + '°')
            drehG = limitSpeed(relDrehR, maxDrehG)
            schwG = limitSpeed(relSchwR, maxSchwG)

            drehW = limit(drehW + drehG, teleAusrichtung - math.pi / 2, teleAusrichtung + math.pi / 2)
            schwW = limit(schwW + schwG, toRad(-5), toRad(85))

            drehGOut = (drehG / maxDrehG) * 8
            drehGOut = ("x" + str(drehGOut)).encode()
            schwGOut = (schwG / maxSchwG) * 8
            schwGOut = ("y" + str(schwGOut)).encode()
            print(drehGOut)
            datenOut.write(drehGOut)
            print(schwGOut)
            datenOut.write(schwGOut)

            '''reset()
            speed(0)
            ht()
            left(90)

            right(toDeg(drehW))
            color('green')
            width(9)
            forward(100)
            up()
            left(toDeg(drehW))
            goto(0, 0)
            down()

            right(toDeg(drehR))
            color('red')
            width(5)
            forward(200)
            up()
            left(toDeg(drehR))
            goto(0, 0)
            down()

            right(toDeg(teleAusrichtung))
            color('blue')
            width(1)
            forward(300)
            up()
            left(toDeg(teleAusrichtung))
            goto(0, 0)
            down()'''
    print(interval - ((time() - starttime) % interval))
    sleep(interval - ((time() - starttime) % interval))
    print("\n")
datenOut.close()
