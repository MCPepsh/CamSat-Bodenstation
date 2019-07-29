import serial
import time

print ("start")
ser = serial.Serial("COM4",9600)

time.sleep(1)
i=0

while i<21:
    print(i)
    ser.write(str(i).encode())
    i=i+1
    time.sleep(1)
    #print(ser.read())

ser.close()
