from app.sensors import Camera
from os.path import isdir


class TestCamera:
    """
    Test Camera module, does not use unit test as it causes out of resources errors
    """
    def test_create_folder(self):
        test_dir = "./images/test"
        c = Camera(test_dir)
        isdir(test_dir)

    def test_take_picture(self):
        c = Camera()
        print(c.take_picture(2.5))


tc = TestCamera()

tc.test_create_folder()

tc.test_take_picture()