import RPi.GPIO as GPIO
from time import sleep

class MotionSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        """
        Reads data from input sensor
        :return: Returns boolean value if basic_return is set to True, or a dictionary with object information.
        """
        return GPIO.input(self.pin)

m = MotionSensor(21)

while True:
    print(m.read())
    sleep(1)