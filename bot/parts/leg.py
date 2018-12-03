import Adafruit_PCA9685 as Hat
from time import sleep

class Leg:
    """ Class for controlling 3 servo motors and provides functions for general Leg movements"""
    SERVO_MIN = 150
    SERVO_MAX = 600
    SERVO_MID = int((SERVO_MAX + SERVO_MIN) / 2)
    SERVO_FREQUENCY = 60
    SERVO_TIMEOUT = 0.5

    def __init__(self, upper_channel, middle_channel, lower_channel, leg_position=''):
        """
        Creating the class is initilised on setting the 3 channels of the leg
        :param upper_channel: The motor that is housed on the upper part of the leg, controls horizontal movement
        :param middle_channel:
        :param lower_channel:
        :param leg_position: String Used to identify which leg it is
        """
        self.servo_motors = {
            "upper": int(upper_channel),
            "middle": int(middle_channel),
            "lower": int(lower_channel)
        }

        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Hat.PCA9685()
        self.pwm.set_pwm_freq(self.SERVO_FREQUENCY)
        print(self.SERVO_MID)


    def __set_motors(self, servo_position=None):
        """
        Method for setting all object servo motors to the same position
        :param servo_position: Servo Motor Voltage Frequency
        :return: None
        """
        for servo_name, servo_channel in self.servo_motors.items():
            print("Setting Servo: " + str(servo_name))
            self.__move_servo(servo_channel, servo_position)
            sleep(self.SERVO_TIMEOUT)

    def __move_servo(self, servo_channel, servo_position):
        """
        Method for moving a single motor to desired position
        :param servo_channel: Channel that servo is in
        :param servo_position: The position to move the servo for
        :return: None
        """
        self.pwm.set_pwm(servo_channel, 0, servo_position)
        sleep(self.SERVO_TIMEOUT)

    def forward(self):
        self.__move_servo(self.servo_motors['middle'], self.SERVO_MAX)

        self.__move_servo(self.servo_motors['lower'], self.SERVO_MAX)

        self.__move_servo(self.servo_motors['upper'], self.SERVO_MIN)

        self.__move_servo(self.servo_motors['lower'], self.SERVO_MID)

        self.__move_servo(self.servo_motors['middle'], self.SERVO_MID)

    def set_initial_position(self):
        for servo_name, servo_channel in self.servo_motors.items():
            self.__move_servo(servo_channel, self.SERVO_MID)
            sleep(self.SERVO_TIMEOUT)



    def test(self):
        pos = (self.SERVO_MID, self.SERVO_MAX, self.SERVO_MIN, self.SERVO_MID)
        for p in pos:
            self.__set_motors(p)


channels = range(13, 16)

legs = []
print(channels)

leg = Leg(0, 1, 2)

leg.forward()

leg.set_initial_position()