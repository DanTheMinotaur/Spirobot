import unittest
try:
    from app.bot import Movements
except NotImplementedError:
    print("Testing on GPIOless device ignoring errors")
    pass


# Test Movement Validation
class TestMovement(unittest.TestCase):
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

    def test_validate_movement_config(self):
        """ Test Movement Validator """
        m = Movements()
        self.assertTrue(m.validate_instructions(self.movement_config), "Leg Config Method Working")

    # Test Loading Configs
    def test_load_config(self):
        m = Movements()

        self.assertIsNotNone(m.load_config("./config/movements/walk-forward.json"),
                             "Could not load and validate config file")

    def test_load_movements(self):
        """
        Test load multiple configs
        """
        m = Movements()
        m.load_movement_files()
        self.assertIsNotNone(m.movements)

    def test_movement(self):
        """
        Tests walking forward movement
        """
        m = Movements()
        m.make_move("walk-forward")
        self.assertTrue(True)

    def test_save_config(self):
        """
        Test Saving config.
        """
        m = Movements()
        self.assertTrue(m.save_new_movement(self.movement_config, "testconfig"))
        m.set_all_initial()



if __name__ == '__main__':
    unittest.main()