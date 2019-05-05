import json
from datetime import datetime


class Common:
    """
    Class contains common methods for use across application
    """
    @staticmethod
    def load_config(file):
        """
        :param file: JSON file to be loaded.
        :return: dictionary object of file
        """
        try:
            with open(file) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print("Could not find '{}', ending application.".format(file))
            exit()

    @staticmethod
    def save_config(file_name, data_dict):
        with open(file_name, 'w') as json_file:
            json.dump(data_dict, json_file)

    @staticmethod
    def bool_to_on_off(boolean):
        """ Method Return String of boolean value"""
        if boolean:
            return "on"
        return "off"

    @staticmethod
    def time_string(date_split: str = '/'):
        """ Returns Preformatted datetime string of current time"""
        return datetime.now().strftime("%d||%m||%YT%H:%M:%S").replace('||', date_split)