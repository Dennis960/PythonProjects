from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from qt_thread_updater import get_updater

import pyautogui
import keyboard
import time
from qt_setup import *

fishClickPosition = (900, 600)
fishTankY = 1128
fishTankStart = 1050
fishTankEnd = 1500
fishTankBorderPosition = (1549, 1175)
fishTankBorderColor = (210, 154, 124)
linePosition1 = (1238, 661)
linePosition2 = (1238, 665)
lineColor = (152, 26, 5)
exclamationMarkPosition = (1268, 525)
exclamationMarkColor = (200, 202, 223)

fishYellowColor = (225, 160, 48)

def areColorsSimilar(color1, color2, threshold=20):
    return abs(color1[0] - color2[0]) < threshold and abs(color1[1] - color2[1]) < threshold and abs(color1[2] - color2[2]) < threshold

def click(pos, duration=0.1):
    x = pos[0]
    y = pos[1]
    pyautogui.mouseDown(x, y)
    time.sleep(duration)
    pyautogui.mouseUp(x, y)

def rightClick(pos, duration=0.1):
    x = pos[0]
    y = pos[1]
    pyautogui.mouseDown(x, y, button="secondary")
    time.sleep(duration)
    pyautogui.mouseUp(x, y, button="secondary")

def isTankVisible(screen):
    color = screen.getpixel(fishTankBorderPosition)
    return areColorsSimilar(color, fishTankBorderColor)

def isLineOut(screen):
    color1 = screen.getpixel(linePosition1)
    color2 = screen.getpixel(linePosition2)
    return areColorsSimilar(color1, lineColor) or areColorsSimilar(color2, lineColor)

def isFishReady(screen):
    color = screen.getpixel(exclamationMarkPosition)
    return areColorsSimilar(color, exclamationMarkColor)

def lineOut():
    rightClick(fishClickPosition, duration=0.5)

def isFishYellow(screen):
    for x in range(fishTankStart, fishTankEnd):
        y = fishTankY
        color = screen.getpixel((x, y))
        if areColorsSimilar(color, fishYellowColor):
            return True
    return False

isLineDragging = False

def dragLine():
    global isLineDragging
    pyautogui.mouseDown(fishClickPosition[0], fishClickPosition[1], button="secondary")
    isLineDragging = True

def releaseLine():
    global isLineDragging
    pyautogui.mouseUp(fishClickPosition[0], fishClickPosition[1], button="secondary")
    isLineDragging = False

click(fishClickPosition)

boxes = []
boxIndex = 0
labels = []
labelIndex = 0
window = None
fishCountLabel = None

def setup(_window: QMainWindow):
    global fishCountLabel, window
    window = _window
    fishCountLabel = QtWidgets.QLabel("Fish count: 0", window)
    fishCountLabel.resize(300, 300)
    fishCountLabel.setStyleSheet("font-size: 20px; color: green;")
    fishCountLabel.move(1000, 100)
    fishCountLabel.show()
    # create 10 boxes
    for _ in range(10):
        box = QtWidgets.QWidget(window)
        boxes.append(box)
        box.setStyleSheet("background-color: transparent; border: 1px solid green;")
    # create 10 labels
    for _ in range(10):
        label = QtWidgets.QLabel("Continuous Count: 0", window)
        labels.append(label)
        label.setStyleSheet("font-size: 20px; color: green; background-color: black;")

def drawBox(pos, size, thickness, centered=True):
    global boxIndex
    # draw green wireframe box
    box = boxes[boxIndex]
    boxIndex = boxIndex + 1
    if centered:
        pos = (int(pos[0] - size[0] / 2), int(pos[1] - size[1] / 2))
    get_updater().call_latest(box.setGeometry, pos[0], pos[1], size[0], size[1])
    get_updater().call_latest(box.setStyleSheet, "background-color: transparent; border: " + str(thickness) + "px solid green;")
    get_updater().call_latest(box.show)

def drawLabel(pos, text):
    global labelIndex
    pos = (pos[0] + 10, pos[1] + 10)
    label = labels[labelIndex]
    labelIndex = labelIndex + 1
    get_updater().call_latest(label.move, pos[0], pos[1])
    get_updater().call_latest(label.setText, text)
    get_updater().call_latest(label.adjustSize)
    get_updater().call_latest(label.show)

def hideAllBoxes():
    global boxIndex
    boxIndex = 0
    for box in boxes:
        get_updater().call_latest(box.hide)

def hideAllLabels():
    global labelIndex
    labelIndex = 0
    for label in labels:
        get_updater().call_latest(label.hide)


def run(is_alive):
    fps = 0
    fishCount = 0
    paused = False
    is_alive.set()
    while is_alive.is_set():
        startTime = time.time()
        if keyboard.is_pressed('q'):
            QtWidgets.qApp.quit()
        if keyboard.is_pressed('p'):
            paused = not paused
            if paused:
                drawLabel((1000, 100), "Paused")
            else:
                hideAllLabels()
            time.sleep(1)
        if paused:
            continue

        screen = pyautogui.screenshot()
        _isFishReady = isFishReady(screen)
        _isTankVisible = isTankVisible(screen)
        _isFishYellow = isFishYellow(screen)
        _isLineOut = isLineOut(screen)
        hideAllBoxes()
        hideAllLabels()
        drawLabel((1000, 200), "FPS: " + str(fps))
        if (_isLineOut and not _isTankVisible):
            if _isFishReady:
                rightClick(fishClickPosition)
                fishCount = fishCount + 1
                get_updater().call_latest(fishCountLabel.setText, "Fish count: " + str(fishCount))
                time.sleep(1)
            else:
                drawBox(exclamationMarkPosition, (10, 10), 2)
                drawLabel(exclamationMarkPosition, "Waiting for fish to get ready")
        if (_isTankVisible):
            drawBox(fishTankBorderPosition, (10, 10), 2)
            drawLabel(fishTankBorderPosition, "Tank is visible")
            drawBox((fishTankStart, fishTankY-20), (fishTankEnd - fishTankStart, 40), 2, centered=False)
            if (_isFishYellow):
                dragLine()
                drawLabel((fishTankStart, fishTankY+20), "Yellow")
            else:
                releaseLine()
                drawLabel((fishTankStart, fishTankY+20), "Red")
        else:
            if isLineDragging:
                releaseLine()
            if not _isLineOut:
                drawBox(linePosition2, (10, 10), 2)
                drawLabel(linePosition2, "Checking line")

        if not _isLineOut and not _isTankVisible:
            lineOut()
            time.sleep(3)
        endTime = time.time()
        duration = endTime - startTime
        fps = 1/duration

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    setup(window)

    alive = threading.Event()
    th = threading.Thread(target=run, args=(alive,))
    th.start()

    app.exec_()
    alive.clear()