import unittest
from app.connect import Communicate
from app.sensors import MotionArray, ProximitySensors


class TestSensorCommunication(unittest.TestCase):

    def test_proximity(self):
        c = Communicate()
        p = ProximitySensors()
        sensor_values = p.read_sensors()
        print("Proximity Sensor Values: {}".format(sensor_values))
        c.send_proximity_data(sensor_values)

    # def test_motion(self):
    #     c = Communicate()
    #     m = MotionArray()
    #     sensor_values = m.detect_motion(10)
    #     print("Motion Sensor Values: {}".format(sensor_values))
    #     c.send_motion_data(sensor_values)

if __name__ == '__main__':
    unittest.main()