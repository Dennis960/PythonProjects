from tkinter import *
import time

width = 1000
height = 1000
x = 0
y = 0
r = 255
g = 0
b = 0
color = "#000000"

def updatePosition():
    global x, y, width, height
    x = x+1
    y = y+1
    if x > width or y > height:
        x = 0
        y = 0
def updateColor():
    global r, g, b, color
    if r == 255 and g != 255 and b == 0:
        g = g+1
    if r != 0 and g == 255 and b == 0:
        r = r-1
    if r == 0 and g == 255 and b != 255:
        b = b+1
    if r == 0 and g != 0 and b == 255:
        g = g-1
    if r != 255 and g == 0 and b == 255:
        r = r+1
    if r == 255 and g == 0 and b != 0:
        b = b-1
    color = '#%02X%02X%02X' % (r, g, b)
def draw():
    for i in range(0, 1000):
        canvas.create_line(x, 0, 0, y, fill=color)
        updatePosition()
        updateColor()
    root.after(1, draw)

root = Tk()
canvas = Canvas(root, width=width, height=height)
canvas.pack()

root.after(1, draw)
root.mainloop()