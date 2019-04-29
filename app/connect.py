import firebase_admin
from firebase_admin import credentials, db, storage
from app.utils import Common
from os.path import basename


class Communicate(Common):
    """
    Class handles communication with Firebase live database
    """
    def __init__(self, private_key: str = "./certs/admin-key.json", firebase_url: str = "https://spirobot-d9387.firebaseio.com/", storage_bucket_url: str = "spirobot-d9387.appspot.com"):
        firebase_admin.initialize_app(credentials.Certificate(private_key), {
            "databaseURL": firebase_url,
            "storageBucket": storage_bucket_url
        })
        self.root = db.reference("/")
        self.__verify_control_details()
        self.__controls = db.reference("controls")
        self.__events = db.reference("events")
        self.__status = db.reference("status")
        self.__video = db.reference("controls/video")
        self.__video_state = None
        self.communication_controls = {}
        self.storage_bucket = storage.bucket()

    def upload_image(self, image_location: str, image_name: str = None):
        if image_name is None:
            image_name = basename(image_location)
        print(image_location)
        print(image_name)

        image_blob = self.storage_bucket.blob(image_name)
        image_blob.upload_from_filename(image_location)
        return image_blob.public_url

    def check_controls(self):
        """ Assigns all controls to instance variable to reduce GET requests """
        self.communication_controls = self.__controls.get()

    @staticmethod
    def __valid_config(current_config: dict, correct_config: dict):
        """
        Validates a configuration against what config it should be
        :param current_config: The configuration to check
        :param correct_config: The configuration that is correct
        :return: Boolean
        """
        for config_item in correct_config:
            if config_item not in current_config:
                return False
        return True

    def __verify_control_details(self):
        """
        Method Checks Current Firebase Document to see if it is complete, if it is missing or incomplete then it
        repopulates
        """
        config = self.root.get()  # Current Firebase Config Document
        default_config = Common.load_config("./config/default_structure.json")  # Default config for bot.
        if config is not None:
            for config_item, config_value in default_config.items():
                if config_item not in config or (isinstance(config_value, dict) and not self.__valid_config(config[config_item], default_config[config_item])):
                    self.root.update({
                        config_item: default_config[config_item]
                    })
        else:
            default_config["events"] = self.__format_event("Bot Reconfigured Firebase")
            self.root.set(default_config)

    @staticmethod
    def __format_event(message):
        """ Creates common formatting for messages being sent. """
        return {
            "datetime": Common.time_string(),
            "message": str(message)
        }

    def ping(self, do_ping=None):
        """ Sets ping status of bot to verify its on. """
        if do_ping is not None:
            self.__controls.update({"ping": True})
        else:
            return self.communication_controls["ping"]

    def get_move_command(self):
        """
        Checks if there is a move command waiting then checks if it is valid,
        :return: valid move string, or None if invalid or no move command.
        """
        valid_movements = [
            "forward",
            "backward",
            "left",
            "right"
        ]
        current_move = self.communication_controls["move"]
        self.__controls.update({"move": False})
        if current_move and isinstance(current_move, str):
            current_move = current_move.lower()
            if current_move in valid_movements:
                return current_move
        elif not current_move:
            return None
        else:
            self.add_event("Invalid Move Command: {}".format(current_move))
            return None

    def set_status(self, status):
        """ Sets current status of device """
        self.__status.update(status)

    def get_video(self):
        video_status = self.communication_controls["video"]
        if isinstance(video_status, bool):
            if self.__video_state is None:
                self.__video_state = video_status
            if video_status != self.__video_state:
                self.__video_state = video_status
                self.add_event("Video Mode Switched {}.".format(Common.bool_to_on_off(video_status)))
            return video_status
        else:
            self.add_event("Invalid Video Must be boolean".format(Common.bool_to_on_off(video_status)))
            self.__controls.update({"Video": False})

    def set_video(self, value=False):
        """
        Sets Video Status
        :param value: Boolean value to indicate whether video is being switched on or off.
        """
        if isinstance(value, bool):
            self.__controls.update({"Video": True})
            self.add_event("Video Mode Switched {}".format(Common.bool_to_on_off(value)))
        else:
            raise ValueError("Video can only take a boolean value")

    def clear_events(self):
        self.__events.set({})

    def add_event(self, event):
        """ Adds an event message """
        print(event)
        self.__events.push(self.__format_event(event))