import firebase_admin
from firebase_admin import credentials, db, storage, messaging
from app.utils import Common
from os.path import basename
from time import sleep


class Communicate(Common):
    """
    Class handles communication with Firebase live database
    """
    valid_status_types = [
        "success",
        "info",
        "warning",
        "error"
    ]

    def __init__(self, private_key: str = "./certs/admin-key.json",
                 firebase_url: str = "https://spirobot-d9387.firebaseio.com/",
                 storage_bucket_url: str = "spirobot-d9387.appspot.com"):
        """
        Constructor for Firebase communications
        :param private_key: Private Key JSON file for Firebase
        :param firebase_url: URL of Firebase Instance
        :param storage_bucket_url: URL of Google Cloud Storage Instance.
        """

        firebase_admin.initialize_app(credentials.Certificate(private_key), {
            "databaseURL": firebase_url,
            "storageBucket": storage_bucket_url
        })
        self.root = db.reference("/")
        self.__verify_control_details()
        sleep(1)  # Allows Live DB to be refreshed and stops old commands from being loaded.
        self.__controls = db.reference("controls")
        self.__events = db.reference("events")
        self.__status = db.reference("status")
        self.__images = db.reference("images")
        self.__custom_moves = db.reference("custom_moves")
        self.__motion_data = db.reference("motion_data")
        self.__proximity_data = db.reference("proximity_data")
        self.__message_token = db.reference("token")
        self.__video_state = None
        self.communication_controls = {}
        self.__storage_bucket = storage.bucket()

    @staticmethod
    def __valid_config(current_config: dict, correct_config: dict):
        """
        Validates a configuration against what config it should be
        :param current_config: The configuration to check
        :param correct_config: The configuration that is correct
        :return: Boolean indicating weather config is valid.
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
                if (config_item == "events" and "events" in root_config) or (config_item == "images" and "images" in root_config):  # Skip if events and images already populated
                    continue
                self.root.update({
                    config_item: default_config[config_item]
                })
        else:
            self.root.set(default_config)

        self.set_status("Waiting...")

    def __check_control(self, control: str):
        """
        Helper Method to validate that config control is valid
        :param control: The co
        :return: Boolean indicating if control is valid
        """
        return control in self.communication_controls

    def set_custom_moves(self, custom_move_names: list):
        """
        Tales a list of movement names and uploads to firebase.
        :param custom_move_names: List of names of movements
        :return: the Firebase list of names with ID's
        """
        for move in custom_move_names:
            self.__custom_moves.push(move)
        return self.__custom_moves.get()

    def ping(self, do_ping: bool = None):
        """
        Sets ping status of bot to verify its on.
        :param do_ping optional value that tells it to ping Firebase if not None
        """
        if do_ping is not None:
            self.__controls.update({"ping": True})
        else:
            return self.communication_controls["ping"]

    def get_mode(self):
        """
        Gets the currently set mode of the bot and returns it, if invalid resets the mode to default
        # :return: 3 possible values for auto_mode true, false or none
        """
        if self.__check_control("auto_mode"):
            selected_mode = self.communication_controls["auto_mode"]
            if isinstance(selected_mode, bool):
                return selected_mode
            elif selected_mode == 0:
                return None
            else:
                self.__controls.update({"auto_mode": 0})
        return None

    def get_move(self):
        """
        Checks if there is a move command waiting then checks if it is valid,
        :return: valid move string, or None if invalid or no move command.
        """

        current_move = self.communication_controls["move"]
        self.__controls.update({"move": False})
        if current_move and isinstance(current_move, str):
            return current_move.lower()
        elif not current_move:
            return None
        else:
            self.add_event("Invalid Move Command: {}".format(current_move), "error")
            return None

    def set_status(self, status: str):
        """
        Sets current status of device
        :param status String of current status.
        """
        print("Status Update: {}".format(status))
        self.root.update({"status": status})

    def set_video(self, video_status: bool = False):
        """
        Sets Video Status
        :param video_status: Boolean value to indicate whether video is on or off.
        """
        print("Setting Video Status")
        self.__controls.update({"video": video_status})

    def get_video(self):
        """
        Checks if the video set command
        :return:
        """
        if self.__check_control("video"):
            return self.communication_controls["video"]

    def get_picture(self):
        """
        Checks if command to take a picture has been set
        :return: True if set, False if not
        """
        return self.__get__control_command("picture")

    def __get__control_command(self, command: str):
        """
        Helper method to get and reset boolean based control command
        :param command:
        :return:
        """
        if self.__check_control(command) and self.communication_controls[command]:
            self.__controls.update({
                command: False
            })
            return True
        return False

    def get_motion_sensor(self):
        """
        Checks the sensor reading command has been set
        :return: Indication weather to read motion sensors
        """
        return self.__get__control_command("read_motion")

    def send_proximity_data(self, proximity_data: dict):
        """
        Sends proximity data to firebase.
        :param proximity_data:
        :return:
        """
        self.__proximity_data.update(proximity_data)

    def send_motion_data(self, motion_data: dict):
        """
        Sends motion data from MotionArray to Firebase
        :param motion_data:
        :return: None
        """
        self.__motion_data.update(motion_data)

    def clear_events(self):
        """
        Clears all events held in Firebase
        """
        self.__events.set({})

    def add_event(self, event: str, status_type: str = "info"):
        """
        Adds an event message
        :param event: The event message to send
        :param status_type: Type of event being triggered, valid ones are: success, info, warning, error
        :return: None
        """
        print("{} Event: {}".format(status_type, event))
        if status_type not in self.valid_status_types:
            status_type = "info"

        self.__events.push({
            "datetime": Common.time_string(),
            "message": event,
            "type": status_type
        })

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
        print(image_blob.path)
        image_url = image_blob.public_url
        self.__images.push(image_url)
        return image_blob.public_url

    def send_notification(self, title: str, body: str):
        """
        Sends a browser notification
        :param title: The title of notification
        :param body: The text to display
        :return: None
        """
        message_token = self.__message_token.get()
        if message_token is not None:
            message = messaging.Message(notification=messaging.Notification(
                title=title,
                body=body
            ), token=message_token)
            response = messaging.send(message)
            print("Browser Notification Send {}".format(response))
        else:
            print("No Message token available...")

    def check_controls(self):
        """ Assigns all controls to instance variable to reduce GET requests """
        self.communication_controls = self.__controls.get()
