from adafruit_servokit import ServoKit
from time import sleep


class Body:

    kit = ServoKit(channels=16)

    def set_all_initial(self):
        """ Sets ALL motors to middle positions aka initial position """
        for channel in range(len(self.kit.servo)):
            self.kit.servo[channel].angle = 90
        sleep(0.3)


class _Leg:
    pass