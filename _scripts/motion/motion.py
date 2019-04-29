from gpiozero import MotionSensor
from time import sleep

motion = MotionSensor(25)

while True:
    print(motion.motion_detected)
    sleep(1)
