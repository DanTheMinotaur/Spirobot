from adafruit_servokit import ServoKit
from time import sleep


class Body:
    kit = ServoKit(channels=16)

    def __init__(self, config):
        self.body_info = config

    def set_all_initial(self):
        for channel in range(len(self.kit.servo)):
            self.kit.servo[channel].angle = 90
        sleep(1)

    def test(self):
        for i in range(len(self.kit.servo)):
            self.kit.servo[i].angle = 180
        sleep(1)
        for i in range(len(self.kit.servo)):
            self.kit.servo[i].angle = 0
        sleep(1)



config = [
    {
      "position": "FRONTLEFT",
      "upper": 0,
      "middle": 1,
      "lower": 2
    },
    {
      "position": "FRONTRIGHT",
      "upper": 3,
      "middle": 4,
      "lower": 5
    },
    {
      "position": "MIDDLELEFT",
      "upper": 6,
      "middle": 7,
      "lower": -1
    },
    {
      "position": "MIDDLERIGHT",
      "upper": 8,
      "middle": 9,
      "lower": -1
    },
    {
      "position": "BACKRIGHT",
      "upper": 10,
      "middle": 12,
      "lower": 11
    },
    {
      "position": "BACKLEFT",
      "upper": 13,
      "middle": 14,
      "lower": 15
    }
]

test_body = Body(config)

test_body.test()

test_body.set_all_initial()
