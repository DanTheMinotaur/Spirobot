import unittest
from app.connect import Communicate


class TestAddEvent(unittest.TestCase):
    """
    Tests create an event and send to browser.
    """
    def test_event(self):
        c = Communicate()
        c.add_event("Tested Config")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()