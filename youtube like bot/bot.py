from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con

nextVideoX = 1096
nextVideoY = 676

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def tryClickImage(imageFileName):
    image = pyautogui.locateOnScreen(imageFileName, grayscale=False, confidence=0.9)
    if image != None:
        click(image.left+3, image.top+3)
    return image != None
def tryClickNextVideoButton():
    win32api.SetCursorPos((nextVideoX,nextVideoY))
    return tryClickImage('nextVideoButton.png')
def tryClickLikeButton():
    if pyautogui.locateOnScreen('likeButtonBlue.png', grayscale=False, confidence=0.9) != None:
        return True
    return tryClickImage('likeButton.png')
def scrollDown():
    win32api.SetCursorPos((970,420))
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 970, 420, -800, 0)
def scrollUp():
    win32api.SetCursorPos((970,420))
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 970, 420, 1000, 0)
def isMaxScrollDown():
    return pyautogui.pixelMatchesColor(1911, 1015, (193, 193, 193), 10)
def isMaxScrollUp():
    return pyautogui.pixelMatchesColor(1911, 131, (193, 193, 193), 10)

wasLikeButtonPressed = False
wasScrolledDown = False
wasScrolledBackUp = False

print("Started")

while not keyboard.is_pressed('q'):
    if not wasLikeButtonPressed:
        if not tryClickLikeButton():
            if not isMaxScrollDown():
                scrollDown()
                wasScrolledDown = True
            else:
                wasLikeButtonPressed = True
                print("no Like Button found")
        if not wasLikeButtonPressed:
            wasLikeButtonPressed = tryClickLikeButton()
    if wasLikeButtonPressed and wasScrolledDown and not wasScrolledBackUp:
        if not isMaxScrollUp():
            scrollUp()
        wasScrolledBackUp = isMaxScrollUp()
    if wasLikeButtonPressed and not wasScrolledDown or wasLikeButtonPressed and wasScrolledDown and wasScrolledBackUp:
        if tryClickNextVideoButton():
            wasLikeButtonPressed = False
            wasScrolledDown = False
            wasScrolledBackUp = False
            sleep(1)


print("Stopped")