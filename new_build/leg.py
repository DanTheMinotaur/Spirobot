from adafruit_servokit import ServoKit
from time import sleep


class Leg:
    kit = ServoKit(channels=16)

    def __init__(self, positions=dict()):
        try:
            self.upper = positions["upper"]
            self.middle = positions["middle"]
            self.name = positions["position"].lower()
            self.motors = (
                self.upper,
                self.middle,
                self.lower
            )
        except KeyError as key:
            print("Positions Config missing key: " + str(key))
            print("Exiting Program")
            exit()

    def test_motor(self, channel=0, angle=90, time=1):
        print("Testing Servo on Channel " + str(channel) + " with an angle of " + str(angle))
        self.kit.servo[channel].angle = angle
        print("Sleeping for " + str(time) + " seconds")
        sleep(time)

    def move_leg_forward(self):
        if "left" in self.name.lower():
            self.kit.servo[self.middle].angle = 160
            self.kit.servo[self.upper].angle = 20
        else:
            self.kit.servo[self.middle].angle = 20
            self.kit.servo[self.upper].angle = 160
        sleep(.5)
        self.kit.servo[self.middle].angle = 90
        sleep(.5)

    def set_initial_position(self):
        for motor in self.motors:
            self.kit.servo[motor].angle = 90


legs = []

config = [
    {
        "name": "frontright",
        "upper": 14,
        "middle": 15
    }
]

for c in config:
    legs.append(Leg(c))

for l in legs:
    if "back" in l.name or "front" in l.name:
        l.set_initial_position()
        l.move_leg_forward()

for l in legs:
    if "back" in l.name or "front" in l.name:
        l.set_initial_position()

"""
FRM = 15
FRU = 14
"""