from bot.parts.leg import Leg
import json

class Body:
    """
    Class Body is for controlling bots movements and sensors
    """
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.bot_details = {}
        self.bot_legs = {}
        self.__setup_legs()

    @staticmethod
    def load_config(json_file="config.json"):
        """
        Method loads a config.json file
        :param json_file: The path to the json config file
        :return: Returns a dictionary object with configuration details
        """
        try:
            with open(json_file) as f:
                config_data = json.load(f)

        except FileNotFoundError:
            json_file = "config.json"

            with open(json_file) as f:
                config_data = json.load(f)
        finally:
            return config_data


    def __setup_legs(self):
        """
        Method sets up each leg from the configuration and creates Leg Objects and assigns them to a dictionary obj
        :return: None
        """

        leg_count = 0
        for leg in self.config["legs"]:
            if "limit" in self.config:
                self.bot_legs[leg["position"]] = Leg(
                    leg["upper"],
                    leg["middle"],
                    leg["lower"],
                    leg["position"],
                    self.config["limit"]
                )
                self.bot_details["limit"] = self.config["limit"]
            else:
                self.bot_legs[leg["position"]] = Leg(
                    leg["upper"],
                    leg["middle"],
                    leg["lower"],
                    leg["position"]
                )
            leg_count += 1

        self.bot_details["leg_count"] = leg_count

    def move_legs(self):
        for leg_position, leg in self.bot_legs.items():
            print("Moving {0} forward".format(leg_position))
            leg.forward()

    def move_motor(self, leg="FRONTLEFT", motor_position="lower", position="SERVO_MAX"):
        try:
            self.bot_legs[leg].move_motor(motor_position, position)
        except KeyError:
            print("Not a valid leg")

    def transport_mode(self):
        self.move_motor("FRONTLEFT", "lower", "SERVO_MAX")
        self.move_motor("FRONTLEFT", "middle", "SERVO_MIN")
        self.move_motor("MIDDLELEFT", "lower", "SERVO_MAX")
        self.move_motor("MIDDLELEFT", "middle", "SERVO_MIN")
        self.move_motor("BACKLEFT", "lower", "SERVO_MAX")
        self.move_motor("BACKLEFT", "middle", "SERVO_MIN")

        self.move_motor("FRONTRIGHT", "lower", "SERVO_MIN")
        self.move_motor("FRONTRIGHT", "middle", "SERVO_MAX")
        self.move_motor("MIDDLERIGHT", "lower", "SERVO_MIN")
        self.move_motor("MIDDLERIGHT", "middle", "SERVO_MAX")
        self.move_motor("BACKRIGHT", "lower", "SERVO_MIN")
        self.move_motor("BACKRIGHT", "middle", "SERVO_MAX")

    def move_forward(self, steps=3):
        print(self.bot_details)
        for i in range(0, steps):
            self.bot_legs["FRONTLEFT"].forward()
            self.bot_legs["FRONTRIGHT"].forward()
            self.bot_legs["MIDDLELEFT"].forward()
            self.bot_legs["MIDDLERIGHT"].forward()
            self.bot_legs["BACKRIGHT"].forward()
            self.bot_legs["BACKLEFT"].forward()

            self.bot_legs["FRONTLEFT"].set_initial_position()
            self.bot_legs["FRONTRIGHT"].set_initial_position()
            self.bot_legs["MIDDLELEFT"].set_initial_position()
            self.bot_legs["MIDDLERIGHT"].set_initial_position()
            self.bot_legs["BACKRIGHT"].set_initial_position()
            self.bot_legs["BACKLEFT"].set_initial_position()

    def set_default_position(self):
        for leg_position, leg in self.bot_legs.items():
            print("Moving {0} to initial".format(leg_position))
            leg.set_initial_position()