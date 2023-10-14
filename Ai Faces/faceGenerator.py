import requests
from PIL import Image
from io import BytesIO
import cv2
import gad
import sys
import subprocess
import math
import time
import keyboard
import re

def getRandomFace():
    url = 'https://thispersondoesnotexist.com/image'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save('img.jpg')
    return img

def getAgeAndGender():
    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn=frame.copy()
        frameHeight=frameOpencvDnn.shape[0]
        frameWidth=frameOpencvDnn.shape[1]
        blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections=net.forward()
        for i in range(detections.shape[2]):
            confidence=detections[0,0,i,2]
            if confidence>conf_threshold:
                x1=int(detections[0,0,i,3]*frameWidth)
                y1=int(detections[0,0,i,4]*frameHeight)
                x2=int(detections[0,0,i,5]*frameWidth)
                y2=int(detections[0,0,i,6]*frameHeight)
                return [x1,y1,x2,y2]

    faceProto="gad/opencv_face_detector.pbtxt"
    faceModel="gad/opencv_face_detector_uint8.pb"
    ageProto="gad/age_deploy.prototxt"
    ageModel="gad/age_net.caffemodel"
    genderProto="gad/gender_deploy.prototxt"
    genderModel="gad/gender_net.caffemodel"

    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList=['Male','Female']

    faceNet=cv2.dnn.readNet(faceModel,faceProto)
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    genderNet=cv2.dnn.readNet(genderModel,genderProto)

    video=cv2.VideoCapture('img.jpg' if 'img.jpg' else 0)
    padding=20
    while cv2.waitKey(1)<0:
        hasFrame,frame=video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        faceBox=highlightFace(faceNet,frame)
        if not faceBox:
            return None

        face=frame[max(0,faceBox[1]-padding):
                    min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                    :min(faceBox[2]+padding, frame.shape[1]-1)]

        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]

        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        return age, gender
def isAgeBetween(age, ab):
    return (ab[0] <= age and ab[1] >= age) or (ab[1] <= age and ab[0] >= age)
def getAgeRange(str):
    strA = re.findall('[0-9]+', str)[0]
    strB = re.findall('[0-9]+', str)[1]
    a = int(strA)
    b = int(strB)
    return (a,b)
def generateFace(desiredAge=None, desiredGender=None):
    age = '0-0'
    gender = None
    if desiredAge == None and desiredGender == None:
        img = getRandomFace()
        age, gender = getAgeAndGender()
        ms = int(round(time.time() * 1000))
        imgPath = 'imgs/' + gender[0] + age + str(ms) + '.jpg'
        img.save(imgPath)
    else:
        while (desiredAge != None and not isAgeBetween(desiredAge, getAgeRange(age))) or (desiredGender != None and not gender[0] == desiredGender):
            img = getRandomFace()
            age, gender = getAgeAndGender()
            print(age,gender)
            ms = int(round(time.time() * 1000))
            imgPath = 'imgs/' + gender[0] + age + str(ms) + '.jpg'
            img.save(imgPath)
    
    print('desired person found: ' + age,gender)
    return img, imgPath

F='F'
M='M'

img, imgPath = generateFace(desiredAge=16, desiredGender=F)
image = cv2.imread(imgPath)
needsNewPicture = True
while cv2.waitKey(33) != ord('a'):
    cv2.imshow('image', image)
    img, imgPath = generateFace(desiredAge=16, desiredGender=F)
    image = cv2.imread(imgPath)