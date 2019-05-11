from app.app import BotController

try:
    c = BotController()
    c.run()
except KeyboardInterrupt:
    print("Closing from terminal...")
