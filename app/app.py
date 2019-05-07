# from app.bot import Body
from app.connect import Communicate
from time import sleep
from app.sensors import ProximitySensors, Camera, MotionArray
import subprocess


class BotController:
    pass


class Controller(BotController):
    def __init__(self):
        self.communications = Communicate()
        self.camera = Camera()
        self.communications.add_event("Bot Started")
        self.__mode = {
            "auto_mode": None,
            "last_mode": ""
        }
        self.__video_status = {
            "last_video_streaming": False,
            "in_use": False
        }

    def __live_video_stream(self, setting: bool):
        """
        Starts or stops the YouTube Live Stream Docker container and runs in the background.
        :param setting: Boolean to indicate if video should be turned on/off
        """
        command = 'start' if setting else 'stop'
        self.__video_status["in_use"] = setting
        subprocess.Popen("sudo docker {} cam".format(command).split(), stdout=subprocess.PIPE)
        self.communications.add_event("Live Streaming to YouTube {}ing.".format(command))

    def __check_move(self):
        move = self.communications.get_move()
        if move is not None:
            print("MOVING BOT {}".format(move))

    def __check_video(self):
        stream_status = self.communications.get_video()
        if self.__video_status["last_video_streaming"] != stream_status:  # Set initial video status
            self.__video_status["last_video_streaming"] = stream_status
            self.__live_video_stream(stream_status)

    def __check_ping(self):
        """
        Checks the status of the ping and turns if on if its off
        """
        if not self.communications.ping():
            self.communications.ping(True)

    def __check_picture(self):
        """
        Checks if the controlling application wants to take a picture and handles its capture and upload
        Turns off the Live Streaming if enabled as bot can't use the camera at the same time.
        :return:
        """
        if self.communications.get_picture():
            self.communications.set_status("Taking Picture")
            try:
                if self.__video_status["in_use"]:
                    self.__live_video_stream(False)  # Turn off Video Live Stream
                    sleep(13)
                    image_path = self.camera.take_picture(3)
                    self.__live_video_stream(True) # Turn Video Stream back on.
                else:
                    image_path = self.camera.take_picture(3)
                if image_path is not None:
                    image_url = self.communications.upload_image(image_path)
                    if image_url:
                        self.communications.add_event("Image Capture Successful", "success")
            except ValueError:
                self.communications.add_event("Could not capture image, try again", "error")

    def __check_mode(self):
        self.__mode["auto_mode"] = self.communications.get_mode()

    def check_commands(self):
        """
        Checks all commands for bot operation.
        :return:
        """
        self.communications.check_controls()
        self.__check_ping()
        self.__check_mode()
        self.__check_video()
        self.__check_picture()
        if self.__mode["auto_mode"]:
            self.mode_auto()
        elif self.__mode["auto_mode"] is None: # Do Nothing
            self.mode_standby()
        else:
            self.mode_manual()

    def mode_standby(self):
        if self.__check_mode_change():
            self.communications.set_status("Standing By")
            print("Standby Mode Set")

    def mode_auto(self):
        if self.__check_mode_change():
            self.communications.set_status("Bot Auto Mode Set")
            # self.communications.add_event("Auto Mode Set")
            #
            print("Auto Mode Set")

    def mode_manual(self):
        if self.__check_mode_change():
            # self.communications.add_event("Manual Mode Set")
            self.communications.set_status("Piloting Bot")
            print("Manual Mode Set")
            self.__check_move()

    def __check_mode_change(self):
        if self.__mode["auto_mode"] != self.__mode["last_mode"]:
            self.__mode["last_mode"] = self.__mode["auto_mode"]
            return True
        return False

    def run(self, timeout=1):
        while True:
            print("Loop")
            self.check_commands()
            sleep(timeout)