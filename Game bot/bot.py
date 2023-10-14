from pyautogui import *
import pyautogui
import time
import keyboard
import numpy
import random
import win32api, win32con
from PIL import ImageGrab
from mss import mss
from PIL import Image
import cv2
import time
import d3dshot

blockSize = 36
screenWidth = 1430
screenHeight = 820
freezeColor = numpy.array([68,68,68,255])
backgroundColor = numpy.array([131,131,131,255])
hookableColor = numpy.array([102,141,157,255])
hookableEdgeColor = numpy.array([56,78,87,255])
unhookableColor = numpy.array([134,126,125,255])
teleportColor = numpy.array([96,96,143,255])

blockOffset = 8

d = d3dshot.create(capture_output="numpy")

def searchForStart(startX, startY):
    ySearchOffset = 14
    for x in range(startX, screenWidth, 9):
        color = frame[startY,x]
        color2 = frame[startY + ySearchOffset,x]
        if (color == hookableColor).all() or (color2 == hookableColor).all():
            if (color2 == hookableColor).all():
                startY += ySearchOffset
            i = 0
            #find edge in x
            while not (frame[startY,x-i] == hookableEdgeColor).all() and i < blockSize:
                i += 1
            startX = x - i
            #find edge in y
            while not (frame[startY-i,x] == hookableEdgeColor).all() and i < blockSize:
                i += 1
            startY = startY - i
            if not (frame[startY,startX] == hookableEdgeColor).all():
                continue
            return (startX % blockSize, startY % blockSize)

print("Started")
iteration = 0
while not keyboard.is_pressed('q'):
    iteration += 1
    textString = ""
    startX = blockSize
    startY = 400
    oldTime = time.time()
    #get image
    with mss() as sct:
        monitor = {"top": 170, "left": 160, "width": screenWidth, "height": screenHeight}
        frame = numpy.array(sct.grab(monitor))
    # frame = d.screenshot()
    #finds top right edge of block
    startXY = searchForStart(startX, startY)
    if startXY == None:
        print("No startPixel found")
        continue
    startX = startXY[0]
    startY = startXY[1]
    for y in range(startY,screenHeight-blockOffset,blockSize):
        for x in range(startX,screenWidth-blockOffset,blockSize):
            color = frame[y+blockOffset,x+blockOffset]
            if (color == backgroundColor).all():
                textString += " "
            elif (color == freezeColor).all():
                textString += "O"
            elif (color == hookableColor).all():
                textString += "a"
            elif (color == unhookableColor).all():
                textString += "s"
            else:
                color = frame[y+3,x+3]
                if (color == teleportColor).all():
                    textString += "T"
                else:
                    textString += "?"
        textString += "\n"

    print(" " + textString.replace("", " ")[1: -1])
    print('fps: {0}'.format(1 / (time.time()-oldTime)) + ' iteration: {0}'.format(iteration))
print("Stopped")