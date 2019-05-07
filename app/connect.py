import firebase_admin
from firebase_admin import credentials, db, storage
from app.utils import Common
from os.path import basename


class Communicate(Common):
    valid_status_types = [
        "success",
        "info",
        "warning",
        "error"
    ]
    """
    Class handles communication with Firebase live database
    """
    def __init__(self, private_key: str = "./certs/admin-key.json",
                 firebase_url: str = "https://spirobot-d9387.firebaseio.com/",
                 storage_bucket_url: str = "spirobot-d9387.appspot.com"):

        firebase_admin.initialize_app(credentials.Certificate(private_key), {
            "databaseURL": firebase_url,
            "storageBucket": storage_bucket_url
        })
        self.root = db.reference("/")
        self.__verify_control_details()
        self.__controls = db.reference("controls")
        self.__events = db.reference("events")
        self.__status = db.reference("status")
        self.__video_state = None
        self.communication_controls = {}
        self.__storage_bucket = storage.bucket()

    def upload_image(self, image_location: str, image_name: str = None):
        """
        Uploads and image to Google Cloud Storage
        :param image_location: The location on device where the image is stored.
        :param image_name: option name for image, if none then will take image filename
        :return: the public URL of the image being uploaded.
        """
        if image_name is None:
            image_name = basename(image_location)

        image_blob = self.__storage_bucket.blob(image_name)
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
        root_config = self.root.get()  # Current Firebase Config Document
        default_config = Common.load_config("./config/default_structure.json")  # Default config for bot.
        if root_config is not None:
            for config_item, config_value in default_config.items():
                if config_item == "events" and "events" in root_config:
                    break
                self.root.update({
                    config_item: default_config[config_item]
                })
        else:
            self.root.set(default_config)

        self.set_status("Waiting...")

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
        self.root.update({"status": status})

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
            self.__controls.update({"video": True})
            self.add_event("Video Mode Switched {}".format(Common.bool_to_on_off(value)))
        else:
            raise ValueError("Video can only take a boolean value")

    def picture(self):
        if "picture" in self.communication_controls and self.communication_controls["picture"]:
            self.__controls.update({
                "picture": False
            })
            return True

    def clear_events(self):
        self.__events.set({})

    def add_event(self, event: str, status_type: str = "info"):
        """
        Adds an event message
        :param event: The event message to send
        :param status_type:
        :return: None
        """
        print(event)
        if status_type not in self.valid_status_types:
            status_type = "success"

        self.__events.push({
            "datetime": Common.time_string(),
            "message": event,
            "type": status_type
        })