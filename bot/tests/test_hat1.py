import Adafruit_PCA9685 as Hat
from time import sleep

servo_min = 150
servo_max = 600

pwm = Hat.PCA9685()

channels = [1, 2, 3]



pwm.set_pwm(0, 0, servo_max)
sleep(1)

pwm.set_pwm(0, 0, servo_min)
sleep(1)
