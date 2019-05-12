from app.connect import Communicate

"""
Tests sending a browser notification 
"""
c = Communicate()

c.send_notification("Test", "Browser Notification")