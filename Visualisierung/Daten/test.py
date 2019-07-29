import random

lat = 55.7080
lon = 42.4452
hig = 1000.0

while (True):
    randLat = random.randint(-20, 20) / 1000.0
    randLon = random.randint(-20, 20) / 1000.0
    randHig = random.randint(-15000, -5000) / 1000.0
    lat += randLat
    lon += randLon
    hig += randHig
    if (hig <= 10.0):
            hig = 1000.0
    
