# from app.bot import Body
from app.connect import Communicate
from time import sleep
from app.sensors import ProximitySensors, Camera


class Controller:
    def __init__(self):
        self.communications = Communicate()
        self.camera = Camera()
        # self.bot = Body()
        self.communications.add_event("Device Started")
        self.__manual_mode = None
        self.__last_video_streaming = None

    def __check_move(self):
        move = self.communications.get_move_command()
        if move is not None:
            print("MOVING BOT {}".format(move))

    def __check_video(self):
        stream_status = self.communications.get_video()
        if self.__last_video_streaming is None or self.__last_video_streaming != stream_status:  # Set initial video status
            self.__last_video_streaming = stream_status
            if stream_status:
                print("Running Youtube Live PLACEHOLDER FOR BASH COMMAND")
            else:
                print("Stopping Video Streaming")

    def __check_ping(self):
        """
        Checks the status of the ping and turns if on if its off
        """
        if not self.communications.ping():
            self.communications.ping(True)

    def check_picture(self):
        if self.communications.picture():
            self.communications.set_status("Taking Picture")
            if self.__last_video_streaming:
                image_path = self.camera.take_picture()
            else:
                image_path = self.camera.take_picture(3)
            if image_path is not None:
                image_url = self.communications.upload_image(image_path)
                if image_url:
                    self.communications.add_event("Image Capture Successful")

    def check_commands(self):
        self.communications.check_controls()
        self.__check_ping()
        self.__check_video()
        self.__check_move()
        self.check_picture()

    def mode_auto(self):
        self.communications.add_event("Auto Mode Set")
        print("Placeholder")

    def mode_manual(self):
        self.communications.add_event("Manual Mode Set")
        self.communications.set_status("")
        print("Placeholder")

    def run(self, timeout=3):
        while True:
            print("Loop")
            self.check_commands()
            sleep(timeout)