from bot.parts.leg import Leg
import json

class Body:
    @staticmethod
    def load_config(json_file='config.json'):
        config_data = None
        with open(json_file) as f:
            config_data = json.load(f)
        return config_data
