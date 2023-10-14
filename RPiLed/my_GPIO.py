BCM = 'BCM'
OUT = 'OUT'
IN = 'IN'
HIGH = 1
LOW = 0

setupPins = []

def setmode(someArgument):
    print('GPIO mode', someArgument)

def setup(pin, mode):
    setupPins.append(pin)
    print(pin, mode)
def output(pin, mode):
    if pin in setupPins:
        print(pin, mode)
    else:
        print('pin not setup!')
class PWM():
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        print('pwm', pin, 'frequency', frequency)
    def start(self, brightness):
        self.brightness = brightness
        print('pwm start', self.pin, 'brightness', brightness)
    def ChangeFrequency(self, frequency):
        self.frequency = frequency
        print('change', self.pin, 'frequency', frequency)