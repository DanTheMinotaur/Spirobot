import unittest
try:
    from app.bot import Movements
except NotImplementedError:
    print("Testing on GPIOless device ignoring errors")
    pass


# Test Movement Validation
class TestMovement(unittest.TestCase):
    def test_validate_movement_config(self):
        movement_config = [{
            "instructions": [
                {
                    "movement": "up",
                    "limit": 0,
                    "wait": 0.1
                },
                {
                    "movement": "forward",
                    "limit": 0,
                    "wait": 0.1
                },
                {
                    "movement": "down",
                    "limit": 0,
                    "wait": 0
                }
            ],
            "sequence": [
                "rightfront",
                "rightback",
                "leftmiddle",
                "leftfront",
                "leftback",
                "rightmiddle"
            ]
        }]
        m = Movements()
        self.assertTrue(m.validate_instructions(movement_config), "Leg Config Method Working")

    def test_load_config(self):
        m = Movements()

        self.assertIsNotNone(m.load_config("./config/movements/walk-forward.json"),
                             "Could not load and validate config file")

    def test_load_movements(self):
        m = Movements()
        m.load_movement_files()
        self.assertIsNotNone(m.movements)

if __name__ == '__main__':
    unittest.main()