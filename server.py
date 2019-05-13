from picamera import PiCamera
import cv2 as cv
from flask import Flask
from flask import make_response
import time
import numpy as np
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World! Welcome to PiPy Imaging API"

@app.route("/still")
def still():
    res = (640, 480)
    with PiCamera(resolution=res) as pcam:
        time.sleep(2)
        img = np.empty((res[1], res[0], 3), dtype=np.uint8)
        pcam.capture(img, 'rgb')

        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        retval, buffer = cv.imencode('.jpg', img)
        response = make_response(buffer.tobytes())
        response.headers.set('Content-Type', 'image/jpeg')
        #response.headers.set('Content-Disposition', 'attachment', filename='still.jpg')
        
        return response

@app.route("/video")
def video():
    return "Works in Progress, this is where video of defined length will be returned"

@app.route("/live")
def live():
    return "Works in Progress, this is where live preview will be returned"

