from app.sensors import ProximitySensors
from time import sleep
p = ProximitySensors()

while True:
    print(p.read_sensors())
    sleep(1)