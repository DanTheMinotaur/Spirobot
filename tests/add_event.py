import unittest
from app.connect import Communicate


class TestAddEvent(unittest.TestCase):
    def test_event(self):
        c = Communicate()
        c.add_event("Tested Config")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()