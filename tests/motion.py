from app.sensors import MotionArray
import unittest


class TestMotion(unittest.TestCase):
    """
    Tests motion array class, needs motion detected to be verified.
    """
    def test_motion_array(self):
        m = MotionArray()
        results = m.detect_motion(10)
        print(results)
        self.assertIsNotNone(results)


if __name__ == '__main__':
    unittest.main()