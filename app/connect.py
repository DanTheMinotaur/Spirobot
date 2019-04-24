import firebase_admin
from firebase_admin import credentials, db
from app.utils import Common

class Communicate(Common):
    """
    Class handles communication with Firebase live database
    """
    def __init__(self, private_key="./certs/admin-key.json", firebase_url="https://spirobot-d9387.firebaseio.com/"):
        firebase_admin.initialize_app(credentials.Certificate(private_key), {
            "databaseURL": firebase_url
        })
        self.ref = db.reference("/")
        self.__verify_control_details()
        self.__ping = db.reference("ping")
        self.__events = db.reference("events")
        self.__move = db.reference("move")
        self.__status = db.reference("status")
        self.__video = db.reference("video")

    def __verify_control_details(self):
        """
        Method Checks Current Firebase Document to see if it is complete, if it is missing or incomplete then it
        repopulates
        """
        config = self.ref.get()  # Current Firebase Config Document
        default_config = Common.load_config("./config/default_structure.json")  # Default config for bot.
        if config is not None:
            for config_item in default_config:
                if config_item not in config:
                    self.ref.update({
                        config_item: default_config[config_item]
                    })
        else:
            default_config["events"].append(
                self.__format_event("Bot Reconfigured Firebase")
            )
            self.ref.set(default_config)

    @staticmethod
    def __format_event(message):
        """ Creates common formatting for messages being sent. """
        return {
            "datetime": Common.time_string(),
            "message": str(message)
        }

    def ping(self):
        """ Sets ping status of bot to verify its on. """
        self.ref.update({"ping": True})

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
        current_move = self.__move.get()
        self.ref.update({"move": False})
        if current_move and isinstance(current_move, str):
            current_move = current_move.lower()
            if current_move in valid_movements:
                return current_move
        self.add_event("Invalid Move Command: {}".format(current_move))
        return None

    def set_status(self, status):
        """ Sets current status of device """
        self.__status.update(status)

    def get_video(self):
        video_status = self.__video.get()
        if isinstance(video_status, bool):
            self.add_event("Video Mode Switched {}, Streaming on Youtube".format(Common.bool_to_on_off(video_status)))
            return video_status
        else:
            self.add_event("Invalid Video Must be boolean".format(Common.bool_to_on_off(video_status)))
            self.__video.update(False)
            return False

    def set_video(self, value=False):
        """
        Sets Video Status
        :param value: Boolean value to indicate whether video is being switched on or off.
        """
        if isinstance(value, bool):
            self.__video.update(value)
            self.add_event("Video Mode Switched {}".format(Common.bool_to_on_off(value)))
        else:
            raise ValueError("Video can only take a boolean value")

    def add_event(self, event):
        """ Adds an event message """
        self.__events.push(self.__format_event(event))