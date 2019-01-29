from adafruit_servokit import ServoKit
from time import sleep


class Leg:
    kit = ServoKit(channels=16)

    def __init__(self, positions=dict(), time_delay=0.5):
        try:
            self.upper = positions["upper"]
            self.middle = positions["middle"]
            self.name = str(positions["position"]).lower()
            self.motors = (
                self.upper,
                self.middle
            )
            self.time_delay = time_delay
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
        if "left" in self.name:
            self.kit.servo[self.middle].angle = 160
            self.kit.servo[self.upper].angle = 20
        else:
            self.kit.servo[self.middle].angle = 20
            self.kit.servo[self.upper].angle = 160
        sleep(self.time_delay)
        self.kit.servo[self.middle].angle = 90
        sleep(self.time_delay)

    def move_leg_backward(self):
        if "left" in self.name:
            print("LEFT NOT IMPLEMENTED")
            self.kit.servo[self.middle].angle = 160
            self.kit.servo[self.upper].angle = 150
        else:
            self.kit.servo[self.middle].angle = 20
            self.kit.servo[self.upper].angle = 30
        sleep(self.time_delay)
        self.kit.servo[self.middle].angle = 90
        sleep(self.time_delay)

    def walk_forward(self, steps=1):
        for step in range(steps):
            self.move_leg_forward()
            self.move_leg_backward()
            print(str(step) + " step")

    def set_initial_position(self):
        for motor in self.motors:
            self.kit.servo[motor].angle = 90


legs = []

config = [

    {
        "position": "frontright",
        "upper": 0,
        "middle": 11
    },
    {
        "position": "frontleft",
        "upper": 13,
        "middle": 10
    },
    {
        "position": "backright",
        "upper": 1,
        "middle": 2
    },
    {
        "position": "backleft",
        "upper": 4,
        "middle": 3
    },
    {
        "position": "middleleft",
        "upper": 6,
        "middle": 5
    },
    {
        "position": "middleright",
        "upper": 7,
        "middle": 9
    }
]

config1 = [
    {
        "position": "middleright",
        "upper": 8,
        "middle": 7
    }
]

for c in config:
    print(c)
    legs.append(Leg(c))


from threading import Thread


for l in legs:
    print(str(l))

    l.walk_forward(3)
    l.set_initial_position()


"""
Need to resolder 14, 15, 12 , 9
"""