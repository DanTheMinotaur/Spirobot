import unittest
from app.connect import Communicate


class TestControls(unittest.TestCase):
    c = Communicate()
    
    def test_object_creation(self):
        """
        Tests to see if object is created correctly, connecting and restores/repairs Firebase Database
        :return:
        """

        print(self.c.root)
        self.assertTrue(self.c.root)

    def test_controls_get(self):
        self.c.check_controls()
        print(self.c.communication_controls)
        self.assertTrue(self.c.communication_controls)

if __name__ == '__main__':
    unittest.main()