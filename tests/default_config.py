import unittest
from app.connect import Communicate


class TestDefaultConfig(unittest.TestCase):
    """
    Tests add event config
    """
    def test_setup_config(self):
        c = Communicate()
        c.add_event("Tested Config")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()