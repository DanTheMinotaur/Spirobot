from adafruit_servokit import ServoKit
from time import sleep
from app.utils import Common
from os.path import splitext, basename
from os import listdir


class Legs(Common):
    """
    Class contains methods for controlling bot physical actions,
    """
    """ Initial Constants for Servo Motors """
    SERVO_MAX = 160
    SERVO_MIN = 10
    SERVO_MID = 90
    DEFAULT_TIMEOUT = 0.3

    kit = ServoKit(channels=16)

    def __init__(self, legs_config: str = "config/legs.json"):
        """
        Constructor, takes legs config json file.
        :param legs_config:
        """
        self.legs = Common.load_config(legs_config)

    def select_leg(self, name: str):
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

    def _run_movement_sequence(self, legs_sequence: list, step_instructions: list or dict):
        """
        Runs a movement sequence.
        :param legs_sequence: the legs to run the instruction
        :param step_instructions: List or Dictionary of step movements to make on each leg
        :return: None
        """
        # print(legs_sequence)
        # print(step_instructions)
        for leg in legs_sequence:
            for step in step_instructions:
                if isinstance(step, list):
                    self.leg_move(step[0], self.select_leg(leg), limit=step[1], wait=step[2])
                elif isinstance(step, dict):
                    self.leg_move(step["movement"], self.select_leg(leg), step["limit"], step["wait"])

    def leg_move(self, movement, leg, limit=0, wait=0):
        """
        Moves leg in a desired direction based off a string value, used for CLI testing.
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


class Movements(Legs):
    """
    Class will be used to load and render movement json files. Will also potentially contain controls for
    generating movement files.
    """
    movements = {}

    def __init__(self, user_movements_src: str = "./config/movements/"):
        """ Load Leg Constructor """
        super().__init__()
        self.load_movement_files("./config/movements/core/")
        self.load_movement_files(user_movements_src)

    def load_movement_files(self, movements: str):
        """
        Scans a directory loading any json files within it
        :param movements: path of directory to search for files
        """
        for file in listdir(movements):
            if ".json" in file:
                self.load_movement(movements + file)

    def make_move(self, move: str, repeat: int = 1, print_sequence: bool = False):
        """
        Method takes a movement string and runs the corresponding movement configuration.
        :param move: String of movement
        :param repeat: the number of times to repeat the movement
        :param print_sequence: print the raw data of each movement for debugging.
        :return:
        """
        if print_sequence:
            print("Using Movement Config: {}".format(move))

        if self.movements and move in self.movements:
            for iteration in range(repeat):
                if print_sequence:
                    print("Performing instruction {}".format(repeat))

                for current_sequence in self.movements[move]:
                    if print_sequence:
                        print("Current SQ: {}".format(current_sequence))
                    self._run_movement_sequence(
                        current_sequence["sequence"],
                        current_sequence["instructions"]
                    )
                    if "wait" in current_sequence and (isinstance(current_sequence["wait"], int) or isinstance(current_sequence["wait"], float) and current_sequence["wait"] != 0):
                        sleep(current_sequence["wait"])
        else:
            print("No movement for that action found")

    def load_movement(self, movement_file: str):
        """
        Loads a movement file and validates it, if valid it will assign as a valid movement with file name as key.
        :param movement_file:
        """
        movement_config = self.load_config(movement_file)
        if self.validate_instructions(movement_config):
            self.movements[splitext(basename(movement_file))[0]] = movement_config
        else:
            print("Invalid Movement Configuration: {}".format(movement_file))

    def save_new_movement(self, movement_data: dict, movement_name: str):
        """
        Method saves and validates new movement config files.
        :param movement_data: dict with instructions
        :param movement_name: The name to give the movement
        :return: Boolean indicating if file was valid and saved.
        """
        if self.validate_instructions(movement_data):
            self.save_config("{}{}.json".format(movement_data, movement_name), movement_data)
            self.movements[movement_name] = movement_data
            return True
        return False

    @staticmethod
    def validate_instructions(movement_config: str):
        """
        Validates an instruction for the bot
        :param movement_config: Dictionary/JSON object with instructions
        :return: Boolean value if config is valid
        """
        if isinstance(movement_config, list) and len(movement_config) > 0:  # Check if list of instructions
            valid_motions = ["movement", "limit", "wait"]
            for movement in movement_config:
                if isinstance(movement, dict) and "instructions" in movement and "sequence" in movement:  # check if keys are correct
                    if isinstance(movement["instructions"], list) and len(movement["instructions"]) > 0:
                        for motion in movement["instructions"]:
                            for key in motion:
                                if key not in valid_motions:
                                    return False
                    if not isinstance(movement["sequence"], list):
                        return False
        return True

