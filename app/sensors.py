from picamera import PiCamera
from time import sleep
from os.path import isdir
from os import makedirs
from datetime import datetime
from gpiozero import DistanceSensor


class ProximitySensors:
    """
    Class for controlling access to the front and rear distance sensors
    """
    def __init__(self):
        self.__front_sensor = DistanceSensor(23, 24)
        self.__rear_sensor = DistanceSensor(0, 0)

    def read_sensors(self, front: bool = True, rear: bool = True):
        """
        Reads distance sensor values and returns them
        :param front: bool read front distance
        :param rear: bool read rear distance
        :return: Dictionary of front and rear sensor readings
        """
        sensor_data = {}
        if front:
            sensor_data["front"] = self.__front_sensor.distance
        if rear:
            sensor_data["rear"] = self.__rear_sensor.distance
        return sensor_data


class Camera:
    """
    Class is used for controlling the built in camera
    """
    def __init__(self, file_folder: str = "./images"):
        self.__local_image_folder = self.__check_dir(file_folder)
        # self.__camera = PiCamera()
        # self.__camera.resolution = (600, 600)
        # self.__camera.rotation = 270

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

    def take_picture(self, camera_wake_up: float or int = None):
        current_time = datetime.now()
        sub_folder = self.__check_dir(self.__local_image_folder + current_time.strftime('%Y.%m.%d'))
        file_location = "{}{}.jpg".format(sub_folder, current_time)
        camera = PiCamera()
        camera.resolution = (2592, 1944)
        camera.rotation = 270
        camera.start_preview()
        if camera_wake_up is not None:
            sleep(camera_wake_up)
        camera.capture(file_location)
        camera.stop_preview()
        return file_location
