from adafruit_servokit import ServoKit
from time import sleep
from app.utils import Common


class Body(Common):
    """
    Class contains methods for controlling bot physical actions,
    """
    """ Initial Constants for Servo Motors """
    SERVO_MAX = 160
    SERVO_MIN = 10
    SERVO_MID = 90
    DEFAULT_TIMEOUT = 0.3

    kit = ServoKit(channels=16)

    def __init__(self, legs_config="config/legs.json"):
        """
        Constructor, takes legs config json file.
        :param legs_config:
        """
        self.legs = Common.load_config(legs_config)

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

    def set_all_initial(self):
        """ Sets ALL motors to middle positions aka initial position """
        for channel in range(len(self.kit.servo)):
            self.kit.servo[channel].angle = self.SERVO_MID
        sleep(self.DEFAULT_TIMEOUT)

    def move(self, move):
        pass  # TODO add functionality for movements

    def walk_forward(self, steps=2):
        for step in range(steps):
            self.step_forward()

    def turn_left(self):
        step_instructions = (
            ["up", 0, 0.1],
            ["forward", 20, 0]
        )
        legs_sequence = (
            "leftfront",
            "leftback"
        )

        self.__run_movement_sequence(legs_sequence, step_instructions)

        step_instructions = (
            ["up", 0, 0],
        )
        legs_sequence = (
            "rightmiddle",
        )

        self.__run_movement_sequence(legs_sequence, step_instructions)

        step_instructions = (
            ["down", 0, 0],
            ["backward", 30, 0],
        )
        legs_sequence = (
            "leftfront",
            "leftback",
        )
        self.__run_movement_sequence(legs_sequence, step_instructions)


    def step_forward(self):
        step_instructions = (
            ["up", 0, 0.1],
            ["forward", 35, 0],
            ["down", 0, 0],
        )
        legs_sequence = ("rightfront", "rightback", "leftmiddle", "leftfront", "leftback", "rightmiddle")

        self.__run_movement_sequence(legs_sequence, step_instructions)

        step_instructions = (
            ["backward", 30, 0.1],
        )

        self.__run_movement_sequence(legs_sequence, step_instructions)

    def __run_movement_sequence(self, legs_sequence, step_instructions):
        for leg in legs_sequence:
            for step in step_instructions:
                self.leg_move(step[0], self.select_leg(leg), limit=step[1], wait=step[2])

    def leg_move(self, movement, leg, limit=0, wait=0):
        """
        Moves leg in a desired direction based off a string value
        :param movement: String of what way to move the leg
        :param leg: Leg dict object
        :param limit: optional limit of distance to move the leg.
        :param wait: optional time to delay program
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
        elif "middle" in movement:
            servo.angle = self.SERVO_MID
        if wait is not None or wait != 0:
            sleep(wait)

    def test_servo(self, channel, angle=10):
        """
        For specifically testing the servo motor
        :param channel: int Servo Channel
        :param angle: int angle to move motor to
        :return: None
        """
        self.kit.servo[channel].angle = angle


