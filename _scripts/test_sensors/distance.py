from gpiozero import DistanceSensor
from time import sleep

# sensor = DistanceSensor(23, 24)
# Sensor with plastic
# 23 = blue
# 24 = green

sensor = DistanceSensor(23, 24)

while True:
    print('Distance to nearest object is', sensor.distance, 'm')
    sleep(1)
