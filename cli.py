from cement import App, Controller, ex
from bot.parts.body import Body, Leg

class BotController(Controller):
    """ CLI Application for grouping commands for testing purposes"""

    class Meta:
        label = 'bot'
        stacked_type = 'embedded'

    @ex(help='Test Config File')
    def config(self):
        """
        Method will print out the info about the bot config loaded from json file.
        :return:
        """
        bot = Body()
        app.log.info("Bot Config file loaded from JSON file " + str(bot.config))

    @ex(help='Move the legs, in no particular order')
    def move_legs(self):
        bot = Body()
        bot.move_legs()

    @ex(help='Move legs into starting position')
    def set_initial(self):
        bot = Body()
        bot.set_default_position()

    @ex(help='Test the percentage calulation function')
    def percent_test(self, percent=10):
        leg = Leg(0,0,0, "TEST")
        print(leg.limit_min_max_motion(percent))

    @ex(help='Make Bot Move Forward')
    def move_forward(self):
        bot = Body()
        bot.move_forward()

    @ex(help='Test a motor on a leg')
    def test_motor(self):
        bot = Body()
        bot.move_motor()

    @ex(help='Curl Bots Legs for transport')
    def transport(self):
        bot = Body()
        bot.transport_mode()

class BotCLI(App):
    class Meta:
        label = 'BotCLI'
        handlers = [
            BotController
        ]


with BotCLI() as app:
    app.run()
