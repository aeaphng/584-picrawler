from pyPS4Controller.controller import Controller
from picrawler.picrawler.picrawler import Picrawler
from vilib import Vilib

# Initialize PiCrawler
crawler = Picrawler()

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

    def on_x_press(self):
        Vilib.take_photo(photo_name="new_photo",path="/andy/Pictures/")

# Connect to PS4 controller
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()