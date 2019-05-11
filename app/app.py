from app.bot import Movements
from app.connect import Communicate
from time import sleep
from app.sensors import ProximitySensors, Camera, MotionArray
import subprocess
from app.utils import Common


class BotController:
    VALID_MOVEMENTS = [
        "forward",
        "backward",
        "left",
        "right"
    ]

    def __init__(self):
        self.communications = Communicate()
        self.proximity_sensors = ProximitySensors()
        self.motion_sensors = MotionArray()
        self.camera = Camera()
        self.bot = Movements()
        self.bot.set_all_initial()
        self.auto_settings = Common.load_config('./config/auto_config.json')
        self.mode = {
            "auto_mode": None,
            "last_mode": ""
        }
        self.__video_status = {
            "last_video_streaming": False,
            "in_use": False
        }
        self.communications.add_event("Bot Started")

    def make_move(self, move: str, repeat: int = 3):
        self.bot.make_move(move, repeat=repeat)

    def turn_left(self):
        self.make_move("left")

    def patrol(self):
        if "patrol_iterations" in self.auto_settings:
            patrol_iterations = self.auto_settings["patrol_iterations"]
        else:
            patrol_iterations = 10

        for iteration in range(patrol_iterations):
            proximity_readings = self.proximity_sensors.read_sensors()
            print("Proximity Readings: {}".format(proximity_readings))
            if proximity_readings["front"] >= self.auto_settings["proximity_threshold"]:
                self.communications.set_status("Moving Forward")
                self.make_move("forward", 2)
            else:
                self.communications.set_status("Object Detected, Avoiding...")
                self.turn_left()

            self.check_subsystem_commands()
            self.__check_mode()
            if self.__check_mode_change():
                return

        self.watch()

    def watch(self):
        """
        Command initialises watch mode, will wait for desired amount of time and set an alert if motion has been triggered.
        """
        self.bot.set_all_initial()
        if "monitor_iterations" in self.auto_settings:
            monitor_iterations = self.auto_settings["monitor_iterations"]
        else:
            monitor_iterations = 10

        monitor_results = self.motion_sensors.detect_motion(read_times=monitor_iterations)
        if monitor_results is None:
            return
        else:
            self.communications.set_status("Motion Detected, PANIC!")
            self.communications.add_event("Motion Triggered on {}".format(monitor_results))

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
        if move is not None and move in self.VALID_MOVEMENTS:
            print("MOVING BOT {}".format(move))
            self.make_move(move)

    def __check_video(self):
        """
        Checks the current video status and compares it if its not currently active then starts/stops live streaming
        :return:
        """
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
                    self.__live_video_stream(True)  # Turn Video Stream back on.
                else:
                    image_path = self.camera.take_picture(3)
                if image_path is not None:
                    image_url = self.communications.upload_image(image_path)
                    if image_url:
                        self.communications.add_event("Image Capture Successful", "success")
            except ValueError:
                self.communications.add_event("Could not capture image, try again", "error")

    def __check_mode(self):
        """ Checks Current Mode Set in Firebase """
        self.mode["auto_mode"] = self.communications.get_mode()

    def check_subsystem_commands(self):
        """
        Checks all non movement related Commands
        :return:
        """
        self.communications.check_controls()
        self.__check_video()
        self.__check_picture()
        self.__check_ping()

    def check_commands(self):
        """
        Checks all commands for bot operation, normal operation.
        :return: None
        """
        self.check_subsystem_commands()
        self._select_mode()

    def _select_mode(self):
        self.__check_mode()
        if self.mode["auto_mode"]:
            self.mode_auto()
        elif self.mode["auto_mode"] is None:  # Do Nothing
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
        self.patrol()

    def mode_manual(self):
        if self.__check_mode_change():
            # self.communications.add_event("Manual Mode Set")
            self.communications.set_status("Piloting Bot")
            print("Manual Mode Set")
        self.__check_move()

    def __check_mode_change(self):
        if self.mode["auto_mode"] != self.mode["last_mode"]:
            self.mode["last_mode"] = self.mode["auto_mode"]
            return True
        return False

    def run(self, timeout=0.25):
        while True:
            print("Loop")
            self.check_commands()
            sleep(timeout)


# class Controller(BotController):
#     def __init__(self):
#         super().__init__()
#         self.communications.add_event("Bot Started")
#         self.__video_status = {
#             "last_video_streaming": False,
#             "in_use": False
#         }
#
#     def __live_video_stream(self, setting: bool):
#         """
#         Starts or stops the YouTube Live Stream Docker container and runs in the background.
#         :param setting: Boolean to indicate if video should be turned on/off
#         """
#         command = 'start' if setting else 'stop'
#         self.__video_status["in_use"] = setting
#         subprocess.Popen("sudo docker {} cam".format(command).split(), stdout=subprocess.PIPE)
#         self.communications.add_event("Live Streaming to YouTube {}ing.".format(command))
#
#     def __check_move(self):
#         move = self.communications.get_move()
#         if move is not None and move in self.VALID_MOVEMENTS:
#             print("MOVING BOT {}".format(move))
#             self.make_move(move)
#
#     def __check_video(self):
#         """
#         Checks the current video status and compares it if its not currently active then starts/stops live streaming
#         :return:
#         """
#         stream_status = self.communications.get_video()
#         if self.__video_status["last_video_streaming"] != stream_status:  # Set initial video status
#             self.__video_status["last_video_streaming"] = stream_status
#             self.__live_video_stream(stream_status)
#
#     def __check_ping(self):
#         """
#         Checks the status of the ping and turns if on if its off
#         """
#         if not self.communications.ping():
#             self.communications.ping(True)
#
#     def __check_picture(self):
#         """
#         Checks if the controlling application wants to take a picture and handles its capture and upload
#         Turns off the Live Streaming if enabled as bot can't use the camera at the same time.
#         :return:
#         """
#         if self.communications.get_picture():
#             self.communications.set_status("Taking Picture")
#             try:
#                 if self.__video_status["in_use"]:
#                     self.__live_video_stream(False)  # Turn off Video Live Stream
#                     sleep(13)
#                     image_path = self.camera.take_picture(3)
#                     self.__live_video_stream(True)  # Turn Video Stream back on.
#                 else:
#                     image_path = self.camera.take_picture(3)
#                 if image_path is not None:
#                     image_url = self.communications.upload_image(image_path)
#                     if image_url:
#                         self.communications.add_event("Image Capture Successful", "success")
#             except ValueError:
#                 self.communications.add_event("Could not capture image, try again", "error")
#
#     def __check_mode(self):
#         self.mode["auto_mode"] = self.communications.get_mode()
#
#     def check_commands(self):
#         """
#         Checks all commands for bot operation.
#         :return:
#         """
#         self.communications.check_controls()
#         self.__check_ping()
#         self.__check_mode()
#         self.__check_video()
#         self.__check_picture()
#         if self.mode["auto_mode"]:
#             self.mode_auto()
#         elif self.mode["auto_mode"] is None: # Do Nothing
#             self.mode_standby()
#         else:
#             self.mode_manual()
#
#     def mode_standby(self):
#         if self.__check_mode_change():
#             self.communications.set_status("Standing By")
#             print("Standby Mode Set")
#
#     def mode_auto(self):
#         if self.__check_mode_change():
#             self.communications.set_status("Bot Auto Mode Set")
#         self.patrol()
#
#     def mode_manual(self):
#         if self.__check_mode_change():
#             # self.communications.add_event("Manual Mode Set")
#             self.communications.set_status("Piloting Bot")
#             print("Manual Mode Set")
#         self.__check_move()
#
#     def __check_mode_change(self):
#         if self.mode["auto_mode"] != self.mode["last_mode"]:
#             self.mode["last_mode"] = self.mode["auto_mode"]
#             return True
#         return False
#
#     def run(self, timeout=0.25):
#         while True:
#             print("Loop")
#             self.check_commands()
#             sleep(timeout)
