print("Run")
from app.app import Controller

try:
    c = Controller()
    c.run()
except KeyboardInterrupt:
    print("Closing from terminal...")
