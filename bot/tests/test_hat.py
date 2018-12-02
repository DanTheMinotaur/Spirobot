import Adafruit_PCA9685 as Hat
from time import sleep

servo_min = 150
servo_max = 600

pwm = Hat.PCA9685()

pwm.set_pwm_freq(60)

channels = [1, 2, 3]

while True:
    for channel in range(3):
        print("Setting min for Channel: " + str(channel))
        pwm.set_pwm(channel, 0, servo_min)
        sleep(1)

    for channel in range(3):
        print("Setting max for Channel: " + str(channel))
        pwm.set_pwm(channel, 0, servo_max)
        sleep(1)
