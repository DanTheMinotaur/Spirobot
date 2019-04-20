from adafruit_servokit import ServoKit
from time import sleep


class Body:
    SERVO_MAX = 160
    SERVO_MIN = 10
    SERVO_MID = 90

    kit = ServoKit(channels=16)

    def set_all_initial(self):
        """ Sets ALL motors to middle positions aka initial position """
        for channel in range(len(self.kit.servo)):
            self.kit.servo[channel].angle = 90
        sleep(0.3)


    def move_leg(self, leg, forward=True):
        leg_pos = str(leg["position"]).lower()
        servo_max = self.SERVO_MAX
        servo_min = self.SERVO_MIN

        if "middle" in leg_pos:
            servo_max -= 20
            servo_min += 20

        print(servo_min)
        print(servo_max)

        if "left" in leg_pos:
            self.kit.servo[leg["lower"]].angle = servo_max
            self.kit.servo[leg["upper"]].angle = servo_min
        else:
            self.kit.servo[leg["lower"]].angle = servo_min
            self.kit.servo[leg["upper"]].angle = servo_max
        sleep(.3)
        self.kit.servo[leg["lower"]].angle = self.SERVO_MID  # Move leg to ground
        #sleep(.3)

    def test_servo(self, channel, angle=10):
        self.kit.servo[channel].angle = angle

    @staticmethod
    def __build_leg(position, upper_channel, lower_channel):
        return {
            "position": str(position),
            "upper": int(upper_channel),
            "lower": int(lower_channel)
        }


class Leg:
    def __init__(self, upper_channel, lower_channel, leg):
        pass


