from adafruit_servokit import ServoKit
from time import sleep
import json


class Body:
    SERVO_MAX = 160
    SERVO_MIN = 10
    SERVO_MID = 90
    DEFAULT_TIMEOUT = 0.3

    kit = ServoKit(channels=16)

    def __organise_legs(self):
        for leg in self.legs:
            if "left" in leg["position"]:
                self.left.append(leg)
            else:
                self.right.append(leg)

    @staticmethod
    def __load_config(file):
        with open(file) as json_file:
            return json.load(json_file)

    def select_leg(self, name):
        """
        Selects Leg by name and returns if, mainly used for testing purposes.
        :param name: Name of leg aka position
        :return: Leg dictionary or None if nothing matches.
        """
        for leg in self.legs:
            if name in leg["position"]:
                return leg
        return None

    def __init__(self, legs_config="config/legs.json"):
        self.legs = self.__load_config(legs_config)
        self.left = list()
        self.right = list()
        self.__organise_legs()

    def set_all_initial(self):
        """ Sets ALL motors to middle positions aka initial position """
        for channel in range(len(self.kit.servo)):
            self.kit.servo[channel].angle = self.SERVO_MID
        sleep(self.DEFAULT_TIMEOUT)

    def walk_forward(self, steps=2):
        for step in range(steps):
            self.step_forward()

    def step_forward2(self):
        for leg in self.legs:
            pass

    def step_forward(self):
        for leg in self.left:
            leg_pos = str(leg["position"])
            if "front" in leg_pos or "back" in leg_pos:
                print(leg)
                self.move_leg(leg)

        for leg in self.right:
            leg_pos = str(leg["position"])
            if "front" in leg_pos or "back" in leg_pos:
                print(leg)
                self.move_leg(leg)

        self.set_all_initial()

    def leg_move(self, movement, leg, limit=0):
        """
        Moves leg in a desired direction based off a string value
        :param movement: String of what way to move the leg
        :param leg: Leg dict object
        :param limit: optional limit of distance to move the leg.
        :return: None
        """
        servo_max = self.SERVO_MAX - limit
        servo_min = self.SERVO_MIN + limit
        if movement in ["up", "down"]:
            servo = self.kit.servo[leg["lower"]]
        else:
            servo = self.kit.servo[leg["upper"]]

        if "up" in movement:
            if "left" in leg["position"]:
                servo.angle = servo_max
            else:
                servo.angle = servo_min
        elif "down" in movement:
            servo.angle = self.SERVO_MID
            """
            if "left" in leg["position"]:
                servo.angle = servo_min
            else:
                servo.angle = servo_max
            """
        elif "forward" in movement:
            if "left" in leg["position"]:
                servo.angle = servo_min
            else:
                servo.angle = servo_max
        elif "backward" in movement:
            if "left" in leg["position"]:
                servo.angle = servo_max
            else:
                servo.angle = servo_min


    def leg_up(self, leg, limit=0):
        servo_max = self.SERVO_MAX - limit
        servo_min = self.SERVO_MIN + limit
        if "left" in leg["position"]:
            self.kit.servo[leg["lower"]].angle = servo_max
        else:
            self.kit.servo[leg["lower"]].angle = servo_min

    def leg_down(self, leg, limit=0):
        servo_max = self.SERVO_MAX - limit
        servo_min = self.SERVO_MIN + limit
        if "left" in leg["position"]:
            self.kit.servo[leg["lower"]].angle = servo_min
        else:
            self.kit.servo[leg["lower"]].angle = servo_max

    def move_leg(self, leg, limit=45):
        leg_pos = str(leg["position"]).lower()
        servo_max = self.SERVO_MAX - limit
        servo_min = self.SERVO_MIN + limit

        if "middle" in leg_pos:  # Set middle legs to less movement so they don't bump into other legs
            servo_max -= 20
            servo_min += 20

        if "left" in leg_pos:
            self.kit.servo[leg["lower"]].angle = servo_max
            self.kit.servo[leg["upper"]].angle = servo_min
        else:
            self.kit.servo[leg["lower"]].angle = servo_min
            self.kit.servo[leg["upper"]].angle = servo_max
        sleep(self.DEFAULT_TIMEOUT)
        self.kit.servo[leg["lower"]].angle = self.SERVO_MID  # Move leg to ground

    def test_servo(self, channel, angle=10):
        """
        For specifically testing the servo motor
        :param channel: int Servo Channel
        :param angle: int angle to move motor to
        :return: None
        """
        self.kit.servo[channel].angle = angle


