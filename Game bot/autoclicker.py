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
import d3dshot
import autopy
from pynput.mouse import Button, Controller

mouse = Controller()
sleep(2)
mouse.position = (100,100)
sleep(1)
autopy.mouse.smooth_move(200,200)