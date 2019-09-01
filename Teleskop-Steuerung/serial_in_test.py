import serial as s
import re

def update():
    a = arduino.read(arduino.in_waiting)
    a = a.decode("utf8")
    a = re.split(", ", a)
    a[0] = re.split(" ", a[0])
    a[1] = re.split(" ", a[1])
    a[0][1] = float(a[0][1]) / 60.0
    a[1][1] = float(a[1][1]) / 60.0
    a[0] = float(a[0][0]) + a[0][1]
    a[1] = float(a[1][0]) + a[1][1]
    return a

arduino = s.Serial("COM4", 9600)
i = 0

while i < 10:
    if arduino.in_waiting > 0:
        daten = update()
        print(daten)
        i+=1
arduino.close()
