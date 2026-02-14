from pyPS4Controller.controller import Controller
from picrawler.picrawler.picrawler import Picrawler
import os
from datetime import datetime
from picamera2 import Picamera2
import time


# Path for saving photos
PHOTO_PATH = "/home/andy/Pictures"

# Ensure the folder exists
os.makedirs(PHOTO_PATH, exist_ok=True)

# Initialize PiCrawler
crawler = Picrawler()


def take_photo():
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    time.sleep(1)  # warm up

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(PHOTO_PATH, f"new_photo_{timestamp}.jpg")

    picam2.capture_file(filename)
    print(f"Saved photo: {filename}")

    picam2.close()

class MyController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # D-Pad up: move forward
    def on_up_arrow_press(self):
        print("Moving Forward")
        crawler.do_action("forward")

    def on_up_arrow_release(self):
        crawler.do_action("stop")

    # D-Pad down: move backward
    def on_down_arrow_press(self):
        print("Moving Backward")
        crawler.do_action("backward")

    def on_down_arrow_release(self):
        crawler.do_action("stop")

    # D-Pad left: turn left
    def on_left_arrow_press(self):
        print("Turning Left")
        crawler.do_action("turn_left")

    def on_left_arrow_release(self):
        crawler.do_action("stop")

    # D-Pad right: turn right
    def on_right_arrow_press(self):
        print("Turning Right")
        crawler.do_action("turn_right")

    def on_right_arrow_release(self):
        crawler.do_action("stop")

    # X button: take photo
    def on_x_press(self):
        print("Taking photo...")
        take_photo()

# Connect to PS4 controller
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
