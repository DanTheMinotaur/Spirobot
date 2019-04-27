import unittest
from app.sensors import Camera
from os.path import isdir


class TestCamera(unittest.TestCase):
    def test_create_folder(self):
        test_dir = "./images/test"
        c = Camera(test_dir)
        self.assertTrue(isdir(test_dir))

    def test_take_picture(self):
        c = Camera()
        self.assertIsNotNone(c.take_picture())

if __name__ == '__main__':
    unittest.main()