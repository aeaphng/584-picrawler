from pyPS4Controller.controller import Controller
from picrawler.picrawler.picrawler import Picrawler
from picamera2 import Picamera2
from flask import Flask, Response
import threading
import os
from datetime import datetime
import cv2
import time
import signal
import sys

# ==============================
# Configuration
# ==============================
PHOTO_PATH = "/home/andy/Pictures"
os.makedirs(PHOTO_PATH, exist_ok=True)

# ==============================
# Initialize Hardware
# ==============================
crawler = Picrawler()
picam2 = Picamera2()

# Configure camera ONCE
camera_config = picam2.create_preview_configuration(
    main={"size": (1280, 720)},
)
picam2.configure(camera_config)
picam2.start()

# Small warmup
time.sleep(1)

# ==============================
# Flask App
# ==============================
app = Flask(__name__)

def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')

@app.route('/mjpg')
def mjpg_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

def take_photo():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(PHOTO_PATH, f"photo_{timestamp}.jpg")

    picam2.capture_file(filename)
    print(f"Saved photo: {filename}")

class MyController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_up_arrow_press(self):
        crawler.do_action("forward")

    def on_up_arrow_release(self):
        crawler.do_action("stop")

    def on_down_arrow_press(self):
        crawler.do_action("backward")

    def on_down_arrow_release(self):
        crawler.do_action("stop")

    def on_left_arrow_press(self):
        crawler.do_action("turn_left")

    def on_left_arrow_release(self):
        crawler.do_action("stop")

    def on_right_arrow_press(self):
        crawler.do_action("turn_right")

    def on_right_arrow_release(self):
        crawler.do_action("stop")

    def on_x_press(self):
        print("Taking photo...")
        take_photo()

def shutdown_handler(sig, frame):
    print("\nShutting down...")
    picam2.stop()
    picam2.close()
    crawler.do_action("stop")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == '__main__':

    flask_thread = threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0',
            port=9000,
            debug=False,
            use_reloader=False
        )
    )
    flask_thread.daemon = True
    flask_thread.start()

    controller = MyController(
        interface="/dev/input/js0",
        connecting_using_ds4drv=False
    )
    controller.listen()
