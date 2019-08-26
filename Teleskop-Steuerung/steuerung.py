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

'''def approxPos(arr):
    out = []
    print(len(arr))
    for item in arr:
        print(item[0])
    print(arr)
    for j in range(3):
        a = 0
        b = 0
        out.append(arr[len(arr) - 1][j])
        for i in range(len(arr) - 1):
            y = arr[i][j]
            weight = 1.0 / (1**(len(arr) - i - 2))
            #print(weight)
            #print(y)
            #print(arr[i+1][j])
            z = arr[i+1][j] - y
            #print(z)
            z = z * weight
            #print(z)
            a = a + z
            b = b + weight
        if(b != 0):
            c = a / b
            out[j] = out[j] + c
    print(arr[len(arr) - 1])
    print(out)
    print([arr[len(arr) - 1][0] - out[0], arr[len(arr) - 1][1] - out[1], arr[len(arr) - 1][2] - out[2]])
    return out'''

def approxPos(arr):
    out = []
    factor = 2
    if len(arr) < 3:
        return arr[len(arr) - 1]

    print()
    for item in arr:
        print(item[0])
    print()
    
    for i in range(3):
        s = []
        for item in arr:
            s.append(item[i])
        out.append(s[len(s) - 1])
        v = []
        a = []
        weight = []
        weighted = []
        for j in range(len(s) - 1):
            weight.append(1/(factor**(len(s) - j - 2)))
            v.append(s[j + 1] - s[j])

        for j in range(len(v) - 1):
            a.append(v[j + 1] - v[j])
            weighted.append(a[j] * weight[j + 1])

        a.append(sum(weighted)/sum(weight[1:]))
        v.append(v[len(v) - 1] + a[len(a) - 1])
        out[i] = (s[len(s) - 1] + v[len(v) - 1])
    return out

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
        delta_lon = delta_lon % toRad(180)
    theta = math.atan2(delta_lon, delta_phi)
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





print(approxPos([[0, 0, 0],
     [1, 1, 1],
     [2, 2, 2],
     [3, 3, 3],
     [4, 4, 4],
     [3, 3, 3],
     [2, 2, 2],
     [3, 3, 3],
     [4, 4, 4],
     [7, 7, 7]]))





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

interval = 1/1          # 1/5 geht noch gut
maxDrehG = toRad(5 * interval)
maxSchwG = toRad(5 * interval)
#maxDrehG = toRad(0.3 * interval)
#maxSchwG = toRad(0.3 * interval)
print(interval)
drehG = 0
schwG = 0
CSDaten = []

#datenOut = serial.Serial("COM4", 115200)
#sleep(3)


starttime = time()
while(not ended):
#for i in range(60):
    with open("../Visualisierung/Visualisierung/aktuelledaten.txt", 'r') as daten:
        daten = daten.readlines()
        if(not len(daten) == 0):
            daten[0] = re.sub("\n", "", daten[0])
            daten[0] = re.split(",", daten[0])
            daten[1] = re.split(",", daten[1])
            akt_pos = [float(daten[1][0]), float(daten[1][1])]
            akt_hig = float(daten[1][2])
            if (len(CSDaten) >= 11):
                CSDaten.pop(0)
                #ended = True
            
            CSDaten.append([float(daten[1][0]), float(daten[1][1]), float(daten[1][2])])
            
            vorhersagen = approxPos(CSDaten)
            CSlatGApr = vorhersagen[0]
            CSlonGApr = vorhersagen[1]
            CShigGApr = vorhersagen[2]
            #print(daten)
            #print(akt_pos)
            #print(akt_hig)

            drehR = geoWinkel(loc, akt_pos)
            print(loc)
            print(akt_pos)
            print([CSlatGApr, CSlonGApr])
            schwR = hoeheWinkel(loc, hig, akt_pos, akt_hig)
            relDrehR = drehR - drehW
            relSchwR = schwR - schwW
            print("relDrehR:....... " + str(toDeg(relDrehR)) + '°')
            print("relSchwR:....... " + str(toDeg(relSchwR)) + '°')
            print("Drehrichtung:... " + str(toDeg(drehR)) + '°')
            print("Schwenkrichtung: " + str(toDeg(schwR)) + '°')
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
            #datenOut.write(drehGOut)
            print(schwGOut)
            #datenOut.write(schwGOut)

            reset()
            speed(0)
            ht()
            left(90)

            right(toDeg(geoWinkel(loc, [CSlatGApr, CSlonGApr])) * 10)
            color('black')
            width(5)
            forward(geoDist([CSlatGApr, CSlonGApr], loc) * 3 / 10.0)
            up()
            left(toDeg(geoWinkel(loc, [CSlatGApr, CSlonGApr])) * 10)
            goto(0, 0)
            down()

            right(toDeg(drehW) * 10)
            color('green')
            width(3)
            forward(geoDist(akt_pos, loc) * 3 / 10.0)
            up()
            left(toDeg(drehW) * 10)
            goto(0, 0)
            down()

            right(toDeg(drehR) * 10)
            color('red')
            width(2)
            forward(geoDist(akt_pos, loc) * 2 / 10.0)
            up()
            left(toDeg(drehR) * 10)
            goto(0, 0)
            down()

            right(toDeg(teleAusrichtung))
            color('blue')
            width(1)
            forward(geoDist(akt_pos, loc) / 10.0)
            up()
            left(toDeg(teleAusrichtung))
            goto(0, 0)
            down()
    print(interval - ((time() - starttime) % interval))
    sleep(interval - ((time() - starttime) % interval))
    print("\n")
#datenOut.close()
