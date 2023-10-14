import time
import win32api, win32con
from PIL import ImageGrab, Image
import imagehash
from math import sqrt
import keyboard

taskDownloadButton = Image.open("TaskDownloadButton.png")
taskDownloadComplete = Image.open("TaskDownloadComplete.png")
taskUploadButton = Image.open("TaskUploadButton.png")
taskGarbagePull = Image.open("TaskGarbagePull.png")
taskFixWires = Image.open("TaskFixWires.png")
taskDivertPower = Image.open("TaskDivertPower.png")
taskDivertPowerSwitch = Image.open("TaskDivertPowerSwitch.png")
taskCalibrate = Image.open("TaskCalibrate.png")
taskStabilizeSteering = Image.open("TaskStabilizeSteering.png")
taskShields = Image.open("TaskShields.png")
taskCard = Image.open("TaskCard.png")
taskManifolds = Image.open("TaskManifolds.png")

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def drag_and_hold(x1, y1, x2, y2, delay=0.1, duration=0):
    win32api.SetCursorPos((x1,y1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
    dx = x2-x1
    dy = y2-y1
    diagonal = int(sqrt(dx*dx+dy*dy))
    for d in range(1, diagonal, 10):
        newX = int(x1 + dx * d/diagonal)
        newY = int(y1 + dy * d/diagonal)
        win32api.SetCursorPos((newX,newY))
        time.sleep(float(delay/diagonal))
    win32api.SetCursorPos((x2,y2))
    time.sleep(duration)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)

def are_images_similar(image1, image2, similarity=4):
    hash = imagehash.average_hash(image1)
    otherhash = imagehash.average_hash(image2)
    return hash - otherhash < similarity

def task_download(screenshot):
    downloadButtonScreenshot = screenshot.crop((871, 642, 896, 674))
    if are_images_similar(downloadButtonScreenshot, taskDownloadButton):
        print("clicking Dowload")
        click(960, 658)
def task_download_complete(screenshot):
    completeScreenshot = screenshot.crop((513, 700, 540, 741))
    if are_images_similar(completeScreenshot, taskDownloadComplete):
        print("closing Downloads")
        click(317, 238)
def task_upload(screenshot):
    uploadButtonScreenshot = screenshot.crop((896, 641, 921, 672))
    if are_images_similar(uploadButtonScreenshot, taskUploadButton):
        print("clicking Upload")
        click(960, 658)

def task_garbage(screenshot):
    pullScreenshot = screenshot.crop((1222, 159, 1246, 204))
    if are_images_similar(pullScreenshot, taskGarbagePull):
        print("pulling Garbage")
        drag_and_hold(1270, 435, 1270, 727, delay=0.1, duration=1.5)
        click(460, 133)

def task_fixWires(screenshot):
    wireScreenshot = screenshot.crop((940, 95, 993, 109))
    if are_images_similar(wireScreenshot, taskFixWires):
        wires = [270, 460, 640, 830]
        wiresStartX = 520
        wiresEndX = 1333
        colors = []
        colors2 = []
        for wire in wires:
            colors.append(screenshot.getpixel((wiresStartX, wire)))
            colors2.append(screenshot.getpixel((wiresEndX, wire)))
        print (colors, colors2)
        for i in range(0, 4):
            color = screenshot.getpixel((wiresStartX, wires[i]))
            for wire2 in range(0, 4):
                if color == colors2[wire2]:
                    startX, startY = wiresStartX, wires[i]
                    endX, endY = wiresEndX, wires[wire2]
                    win32api.SetCursorPos((startX,startY))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,startX,startY,0,0)
                    time.sleep(0.1)
                    win32api.SetCursorPos((endX,endY))
                    time.sleep(0.1)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,endX,endY,0,0)
                    time.sleep(0.2)
                    break

def task_divertPower(screenshot):
    powerScreenshot = screenshot.crop((944, 168, 978, 202))
    if are_images_similar(powerScreenshot, taskDivertPower):
        switches = [592, 688, 784, 880, 976, 1072, 1168, 1265]
        switchStartY = 762
        switchEndY = 670
        targetColor = (255, 98, 0)
        for i in range(0, 8):
            color = screenshot.getpixel((switches[i], switchStartY))
            if color[0] == targetColor[0]:
                win32api.SetCursorPos((switches[i],switchStartY))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,switches[i],switchStartY,0,0)
                time.sleep(0.1)
                win32api.SetCursorPos((switches[i],switchEndY))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,switches[i],switchEndY,0,0)
                click(460, 140)
                break
def task_divertPowerSwitch(screenshot):
    switchScreenshot = screenshot.crop((940, 472, 980, 513))
    if are_images_similar(switchScreenshot, taskDivertPowerSwitch):
        click(960, 550)
        time.sleep(0.3)
        click(340, 270)

def task_calibrate(screenshot):
    calibrateScreenshot = screenshot.crop((680, 204, 724, 246))
    if are_images_similar(calibrateScreenshot, taskCalibrate):
        print("Todo")
    #     bars = [230, 480, 1250]
    #     buttons = [310, 580, 840]
    #     for i in range(0,3):
    #         win32api.SetCursorPos((1200, bars[i]))
    #         while screenshot.getpixel((1200, bars[i]))[0] == 0:
    #             screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    #             print(screenshot.getpixel((1200, bars[i])))
    #             if not screenshot.getpixel((890, 200))[0] == 170:
    #                 return
    #         click(1200, buttons[i])
            
def task_stabilizeSteering(screenshot):
    stabilizeScreenshot = screenshot.crop((922, 116, 1003, 141))
    if are_images_similar(stabilizeScreenshot, taskStabilizeSteering):
        click(960, 540)
        time.sleep(0.1)
        click(463, 136)

def task_shields(screenshot):
    shieldsScreenshot = screenshot.crop((877, 100, 924, 136))
    if are_images_similar(shieldsScreenshot, taskShields):
        shields = [(741, 299), (947, 175), (1180, 301), (960, 426), (704, 552), (1166, 555), (951, 680)]
        for i in range(0, 7):
            if screenshot.getpixel(shields[i])[1] < 100:
                click(shields[i][0], shields[i][1])
                time.sleep(0.1)
        click(450, 144)

def task_card(screenshot):
    cardScreenshot = screenshot.crop((593, 130, 619, 173))
    if are_images_similar(cardScreenshot, taskCard):
        click(719, 815)
        time.sleep(1)
        drag_and_hold(520, 400, 1420, 400, delay= 3)
        time.sleep(0.1)
        click(465, 145)

def task_manifolds(screenshot):
    mainfoldsScreenshot = screenshot.crop((561, 371, 585, 403))
    if are_images_similar(mainfoldsScreenshot, taskManifolds):
        try:
            ys = [395, 550]
            xs = [586, 739, 892, 1045, 1198]
            positions = [((65, 46), (49, 96)), ((52, 46), (66, 78)), ((77, 47), (84, 67)), ((51, 66), (71, 91)), ((53, 37), (49, 62)), ((56, 67), (61, 43)), ((88, 36), (76, 51)), ((52, 74), (78, 72)), ((83, 56), (60, 62)), ((57, 77), (71, 79))]
            buttonDict = {}
            for y in ys:
                for x in xs:
                    for i in range(0, 10):
                        pos1 = (positions[i][0][0] + x, positions[i][0][1]+y)
                        pos2 = (positions[i][1][0] + x, positions[i][1][1]+y)
                        if screenshot.getpixel(pos1)[0] < 100 and screenshot.getpixel(pos2)[0] < 100:
                            buttonDict[i] = (x+60, y+60)
                            break
            for i in range(0,10):
                position = buttonDict[i]
                click(position[0], position[1])
                time.sleep(0.1)
            click(460, 360)
        except:
            pass

while not keyboard.is_pressed('u'):
    startTime = time.time()
    screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    task_download(screenshot)
    task_upload(screenshot)
    task_download_complete(screenshot)
    task_garbage(screenshot)
    task_fixWires(screenshot)
    task_divertPower(screenshot)
    task_calibrate(screenshot)
    task_divertPowerSwitch(screenshot)
    task_stabilizeSteering(screenshot)
    task_shields(screenshot)
    task_card(screenshot)
    task_manifolds(screenshot)
    print("All checks:",time.time() - startTime)