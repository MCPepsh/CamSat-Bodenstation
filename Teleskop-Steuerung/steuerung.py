import serial
import re
import json
import math
import time

def update():
    a = antenne.read(antenne.in_waiting)
    print(a)
    a = a.decode("utf8")
    print(a)
    a = re.split(", ", a)
    a[0] = re.split(" ", a[0])
    a[1] = re.split(" ", a[1])
    a[0][1] = float(a[0][1]) / 60.0
    a[1][1] = float(a[1][1]) / 60.0
    a[0] = float(a[0][0]) + a[0][1]
    a[1] = float(a[1][0]) + a[1][1]
    return a

def toDeg(x):
    return (x / math.pi) * 180

def toRad(x):
    return (x / 180) * math.pi

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

def geoDist(a, b):      # https://www.sunearthtools.com/en/tools/distance.php#txtDist_1
    p1 = [toRad(a[0]), toRad(a[1])]
    p2 = [toRad(b[0]), toRad(b[1])]
    return 6372795.477598 * math.acos(math.sin(p1[0]) * math.sin(p2[0]) + math.cos(p1[0]) * math.cos(p2[0]) * math.cos(p1[1]-p2[1]))

def hoeheWinkel(geo1, h1, geo2, h2):
    a = abs(h1 - h2)
    b = geoDist(geo1, geo2)
    return math.atan2(a, b)

def limitSpeed(n, maxGeschw):
    return max(min(maxGeschw, n), -maxGeschw)


antenne = serial.Serial("COM4", 9600)
drehMotor = serial.Serial("COM5", 9600)
#schwMotor = serial.Serial("COM6", 9600)
time.sleep(1)
maxDrehGeschw = 10
maxSchwGeschw = 10

with open("settings.json", 'r') as settings:
    settings = json.load(settings)
    TelPos = settings["location"]
    TelBlickrichtung = settings["lookingAt"]
    TelHeight = settings["height"]
    drehWinkel = geoWinkel(TelPos, TelBlickrichtung)
    #drehW = settings["drehWinkel"]

    #schwW = math.atan((1000 - hig) / geoDist(loc, lok))
    #schwW = hoeheWinkel(loc, hig, lok, 0)
    schwWinkel = settings["schwenkWinkel"]

i = 0
#for i in range(30):
while i < 30:
    if antenne.in_waiting > 0:
        daten = update()
        print(daten)
        CSPos = float(daten[0]), float(daten[1])
        CSHeight = float(daten[2])
        drehRichtung = geoWinkel(TelPos, CSPos)
        schwRichtung = hoeheWinkel(TelPos, TelHeight, CSPos, CSHeight)
        relDrehRichtung = drehRichtung - drehWinkel
        relSchwRichtung = schwRichtung - schwWinkel
        drehGeschw = int(limitSpeed(relDrehRichtung, maxDrehGeschw))
        schwGeschw = int(limitSpeed(relSchwRichtung, maxSchwGeschw))
        drehMotor.write(drehGeschw)
        #schwMotor.write(schwGeschw)
        i+=1
antenne.close()
drehMotor.close()
#schwMotor.close()
