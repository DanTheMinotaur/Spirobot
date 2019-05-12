from app.connect import Communicate
import unittest


class TestFileUpload(unittest.TestCase):

    def test_upload_image(self, img="./images/test_default_rotation.jpg"):
        """
        Test upload image to Google Cloud Storage.
        """
        c = Communicate()
        print(c.upload_image(img))


if __name__ == '__main__':
    unittest.main()