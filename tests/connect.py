import unittest
from app.connect import Communicate


class TestControls(unittest.TestCase):
    """
    Class test various Firebase Communications mechanisms.
    """
    c = Communicate()

    def test_object_creation(self):
        """
        Tests to see if object is created correctly, connecting and restores/repairs Firebase Database
        """

        print("Object Reference: {}".format(self.c.root))
        self.assertTrue(self.c.root)

    def test_controls_get(self):
        """
        Check if controls are collected from firebase.
        """
        self.c.check_controls()
        print("Current Communcation Controls in Firebase: {}".format(self.c.communication_controls))
        self.assertTrue(self.c.communication_controls)

    def test_get_ping(self):
        """
        Tests collecting ping data
        """
        self.c.check_controls()
        print("Testing initial ping")
        self.assertFalse(self.c.ping())

    def test_get_move(self):
        """
        Tests colllecting move data from firebase
        """
        self.c.check_controls()
        self.assertIsNone(self.c.get_move())

    def test_get_video(self):
        """
        Checks video command
        """
        self.c.check_controls()
        self.assertFalse(self.c.get_video())

    def test_set_video(self):
        """
        Test Set video
        """
        self.c.set_video(True)
        self.c.check_controls()
        self.assertTrue(self.c.get_video())


if __name__ == '__main__':
    unittest.main()