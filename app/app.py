# from app.bot import Body
from app.connect import Communicate
from time import sleep


class Controller:
    def __init__(self):
        self.communications = Communicate()
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

    def check_commands(self):
        self.__check_video()
        self.__check_move()

    def mode_auto(self):
        print("Placeholder for Auto Mode")
        pass

    def mode_manual(self):
        print("Placeholder for Manual Mode")
        pass

    def run(self, timeout=3):
        while True:
            self.check_commands()
            sleep(timeout)