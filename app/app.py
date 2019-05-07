# from app.bot import Body
from app.connect import Communicate
from time import sleep
from app.sensors import ProximitySensors, Camera
import subprocess


class Controller:
    def __init__(self):
        self.communications = Communicate()
        self.camera = Camera()
        # self.bot = Body()
        self.communications.add_event("Bot Started")
        self.__auto_mode = None
        self.__video_status = {
            "last_video_streaming": False,
            "in_use": False
        }
        self.__last_video_streaming = False

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

    def check_commands(self):
        """
        Checks all commands for bot operation.
        :return:
        """
        self.communications.check_controls()
        self.__check_ping()
        self.__check_video()
        self.__check_move()
        self.__check_picture()

    def mode_auto(self):
        self.communications.add_event("Auto Mode Set")
        print("Placeholder")

    def mode_manual(self):
        self.communications.add_event("Manual Mode Set")
        self.communications.set_status("")
        print("Placeholder")

    def run(self, timeout=1):
        while True:
            print("Loop")
            self.check_commands()
            sleep(timeout)