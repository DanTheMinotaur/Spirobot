from picamera import PiCamera
from time import sleep
from os.path import isdir
from os import makedirs
from datetime import datetime

class Camera:
    """
    Class is used for controlling the built in camera
    """
    def __init__(self, file_folder: str = "./images"):
        self.__local_image_folder = self.__check_dir(file_folder)
        self.__camera = PiCamera()
        self.__camera.rotation = 270

    @staticmethod
    def __check_dir(directory: str):
        """
        Checks if a directory exists and creates it if not
        :param directory: string for file going in
        :return:the directory being created.
        """
        if not directory.endswith('/'):
            directory = directory + '/'
        if not isdir(directory):
            makedirs(directory)
        return directory

    def take_picture(self):
        current_time = datetime.now()
        sub_folder = self.__check_dir(self.__local_image_folder + current_time.strftime('%Y.%m.%d'))
        file_location = "{}{}.jpg".format(sub_folder, current_time)
        self.__camera.start_preview()
        sleep(2.5)
        self.__camera.capture(file_location)
        self.__camera.stop_preview()
        return file_location