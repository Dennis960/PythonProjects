try:
    import RPi.GPIO as GPIO
except:
    import my_GPIO as GPIO
import time
import threading
from myLogging import my_print as print
import json
import vars
import os.path

#        r1, g1, b1,   r2, g2, b2  r3, g3, b3    r4, g4, b4
pins = [(17, 6, 27), (5, 26, 22), (15, 18, 14), (24, 25, 23)]
pwms = []
pwmThreads = []

GPIO.setmode(GPIO.BCM)

class JsonSettings():
    def __init__(self):
        if os.path.isfile(vars.PATH_TO_SETTINGS_JSON):
            with open(vars.PATH_TO_SETTINGS_JSON) as jsonFile:
                try:
                    self.data = json.load(jsonFile)
                except:
                    self.data = json.loads('{}')
        else:
            self.data = json.loads('{}')
    def save(self):
        with open(vars.PATH_TO_SETTINGS_JSON, 'w+') as jsonFile:
            json.dump(self.data, jsonFile)
    def set_colorData_at_index(self, stripeIndex, colorIndex, data):
        if not str(stripeIndex) in self.data:
            self.data[str(stripeIndex)] = {}
        self.data[str(stripeIndex)][str(colorIndex)] = data
    def get_colorData_from_index(self, stripeIndex, colorIndex):
        if not str(stripeIndex) in self.data: return None
        if not str(colorIndex) in self.data[str(stripeIndex)]: return None
        else: return self.data[str(stripeIndex)][str(colorIndex)]
    def set_light(self, stripeIndex, colorIndex, alpha, hertz):
        data = {
            'effect' : None,
            'alpha' : alpha,
            'hertz' : hertz
        }
        self.set_colorData_at_index(stripeIndex, colorIndex, data)
        self.save()
    def get_light(self, stripeIndex, colorIndex):
        colorData = self.get_colorData_from_index(stripeIndex, colorIndex)
        if colorData is None: return None
        try:
            if not colorData['effect'] is None:
                return colorData['alpha'], colorData['hertz']
        except:
            return None

    def set_fade(self, stripeIndex, colorIndex, duration):
        data = {
            'effect' : 'fade',
            'duration' : duration
        }
        self.set_colorData_at_index(stripeIndex, colorIndex, data)
        self.save()
    def get_fade(self, stripeIndex, colorIndex):
        colorData = self.get_colorData_from_index(stripeIndex, colorIndex)
        if colorData is None: return None
        try:
            if not colorData['effect'] is 'fade':
                return colorData['duration']
        except:
            return None

def setup_pins_and_threads():
    settings = JsonSettings()
    for stripeIndex, stripe in enumerate(pins):
        stripPwms = ()
        threadRow = []
        for colorIndex, pin in enumerate(stripe):
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 100)
            stripPwms = stripPwms + (pwm,)
            threadRow.append(None)
        pwms.append(stripPwms)
        pwmThreads.append(threadRow)
def apply_saved_settings():
    settings = JsonSettings()
    for stripeIndex, stripe in enumerate(pwmThreads):
        for colorIndex, _ in enumerate(stripe):
            light = settings.get_light(stripeIndex, colorIndex)
            if light is not None:
                alpha, hertz = light
                _raw_set_light(stripeIndex, colorIndex, alpha, hertz)
            fade = settings.get_fade(stripeIndex, colorIndex)
            if fade is not None:
                duration = fade
                start_color_fade(stripeIndex, colorIndex, duration)

def set_light(stripeIndex, colorIndex, alpha, hertz=100):
    JsonSettings().set_light(stripeIndex, colorIndex, alpha, hertz)
    if pwmThreads[stripeIndex][colorIndex] is not None:
        pwmThreads[stripeIndex][colorIndex].stop()
        pwmThreads[stripeIndex][colorIndex] = None
    _raw_set_light(stripeIndex, colorIndex, alpha, hertz)
def _raw_set_light(stripeIndex, colorIndex, alpha, hertz=100):
    pwm = pwms[stripeIndex][colorIndex]
    pwm.start(float(alpha)/2.55)
    pwm.ChangeFrequency(hertz)
def _turn_on_pin(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
def _turn_off_pin(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

class FadeColor(threading.Thread):
    def __init__(self, stripeIndex, colorIndex, duration):
        threading.Thread.__init__(self)
        self._running = True
        self.stripeIndex = stripeIndex
        self.colorIndex = colorIndex
        self.duration = duration
    def calculate_brightness_linear(self):
        return (self.brightness/16)**2
        
    def run(self):
        self.brightness = 0
        increasing = True
        while self._running:
            if self.brightness >= 255:
                increasing = False
            if self.brightness <= 10:
                increasing = True
            self.brightness += 1 if increasing else -1
            _raw_set_light(self.stripeIndex, self.colorIndex, self.calculate_brightness_linear())
            time.sleep(self.duration/255/2/1000)
    def change_duration(self, new_duration):
        self.duration = new_duration
    def change_brightness(self, new_brightness):
        self.brightness = new_brightness
    def stop(self):
        self._running = False

def start_color_fade(stripeIndex, colorIndex, duration):
    JsonSettings().set_fade(stripeIndex, colorIndex, duration)
    if pwmThreads[stripeIndex][colorIndex] is not None:
        pwmThreads[stripeIndex][colorIndex].change_duration(duration)
    else:
        pwmThreads[stripeIndex][colorIndex] = FadeColor(stripeIndex, colorIndex, duration)
        pwmThreads[stripeIndex][colorIndex].start()

def sync_all_fadeColor():
    for stripeThread in pwmThreads:
        for pwmThread in stripeThread:
            if pwmThread is not None:
                pwmThread.change_brightness(0)

def turn_off_all():
    for stripeIndex, stripe in enumerate(pins):
        for colorIndex, _ in enumerate(stripe):
            set_light(stripeIndex, colorIndex, 0)
def turn_on_all():
    for stripeIndex, stripe in enumerate(pins):
        for colorIndex, _ in enumerate(stripe):
            set_light(stripeIndex, colorIndex, 255)
setup_pins_and_threads()
apply_saved_settings()