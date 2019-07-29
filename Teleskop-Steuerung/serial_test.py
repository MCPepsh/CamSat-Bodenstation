import serial as s
import tkinter as tk

arduinoData = s.Serial('COM4', 9600)


def led_on():
    arduinoData.write(b'1')

def led_off():
    arduinoData.write(b'0')

led_control_window = tk.Tk()

btn1 = tk.Button(led_control_window, text = "ON ", command = led_on)
btn2 = tk.Button(led_control_window, text = "OFF", command = led_off)

btn1.grid(row = 0, column = 1)
btn2.grid(row = 1, column = 1)


led_control_window.mainloop()


led_on()

print("done")
