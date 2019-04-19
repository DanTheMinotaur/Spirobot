from adafruit_servokit import ServoKit
from time import sleep


class Leg:
    kit = ServoKit(channels=16)

    def __init__(self, positions=dict()):
        try:
            self.upper = positions["upper"]
            self.middle = positions["middle"]
            self.lower = positions["lower"]
            self.name = positions["position"]
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
            self.kit.servo[self.middle].angle = 170
            self.kit.servo[self.upper].angle = 10
        else:
            self.kit.servo[self.middle].angle = 10
            self.kit.servo[self.upper].angle = 170
        sleep(.5)
        self.kit.servo[self.middle].angle = 90
        sleep(.5)

    def set_initial_position(self):
        for motor in self.motors:
            self.kit.servo[motor].angle = 90


config_left = {
    "position": "FRONTLEFT",
    "upper": 0,
    "middle": 1,
    "lower": 2
}

config_right = {
    "position": "FRONTRIGHT",
    "upper": 3,
    "middle": 4,
    "lower": 5
}

test_left = Leg(config_left)

test_right = Leg(config_right)


test_right.move_leg_forward()
test_left.move_leg_forward()
test_right.set_initial_position()
test_left.set_initial_position()

