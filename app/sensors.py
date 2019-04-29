from picamera import PiCamera
from time import sleep
from os.path import isdir
from os import makedirs
from datetime import datetime
from gpiozero import DistanceSensor, MotionSensor


class MotionArray:
    """
    Class reads an array of Passive Infrared Sensor
    """
    def __init__(self):
        self.__motion_sensors = {
            "right": MotionSensor(25),
            "left": MotionSensor(20),
            "rear": MotionSensor(4),
            "front": MotionSensor(22)
        }

    def detect_motion(self, read_times: int, wait_time: float or int = 0.5):
        """
        Reads all motion sensors in array, for a desired time and returns the results if they are triggered
        :param read_times: The number of times it should read from the sensors
        :param wait_time: The time it should wait between sensor readings.
        :return: dictionary of what sensors have been triggered, if none have been triggered returns empty dict
        """
        results = {}
        for check in range(read_times):
            sleep(wait_time)
            for sensor, sensor_object in self.__motion_sensors.items():
                detected = sensor_object.motion_detected
                if detected:
                    results[sensor] = detected
        return results

    def read_sensor(self, sensor: str):
        """
        Reads a single sensor and returns its value
        :param sensor: Key of sensor to read, "front", "rear", "left" and "right"
        :return: value of sensor or error dictionary
        """
        try:
            return self.__motion_sensors[sensor]
        except KeyError:
            return {"invalid": "{} Is not a valid sensor, valid sensors are: {}".format(sensor, self.__motion_sensors)}


class ProximitySensors:
    """
    Class for controlling access to the front and rear distance sensors
    """
    def __init__(self):
        self.__front_sensor = DistanceSensor(23, 24)
        self.__rear_sensor = DistanceSensor(17, 18)

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
        """
        Takes a picture with the camera sensor.
        :param camera_wake_up: Specify time to give activate camera sensor to activate, specify None if camera
        is already active
        :return: relative file location
        """
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
