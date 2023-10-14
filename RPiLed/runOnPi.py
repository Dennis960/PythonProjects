import pysftp
from myLogging import my_print as print
import os

excludedFiles = ['__pycache__', '.ionide', '.vscode', 'runOnPi.py', 'test.py', 'led.log', 'my_GPIO.py']

def uploadToPi(fromPath, toPath):
    try:
        connection = pysftp.Connection(host="192.168.2.56", username="pi", password='raspberry')
        print('connection established')
        print('uploading from', fromPath, 'to', toPath)
        connection.put(fromPath, toPath)
        connection.close()
    except:
        print('something went wrong')

for filename in os.listdir('../RPiLed'):
    if filename in excludedFiles or filename.endswith('.service') or filename.endswith('.path'):
        continue
    uploadToPi(filename, '/home/pi/Led/' + filename)