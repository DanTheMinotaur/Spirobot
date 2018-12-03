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

    def set_default_position(self):
        for leg_position, leg in self.bot_legs.items():
            print("Moving {0} to initial".format(leg_position))
            leg.set_initial_position()