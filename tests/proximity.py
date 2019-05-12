from app.sensors import ProximitySensors
import unittest


class TestProximity(unittest.TestCase):
    def test_prox(self):
        """
        Test Proximity Sensors
        """
        p = ProximitySensors()
        self.assertIsNotNone(p.read_sensors())


if __name__ == '__main__':
    unittest.main()