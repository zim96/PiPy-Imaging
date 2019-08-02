from picamera import PiCamera
import cv2 as cv
from flask import Flask
from flask import make_response
from flask import Response
from flask import request
import time
import numpy as np
app = Flask(__name__)

def livestream_gen():
	res = (640, 480)
	with PiCamera(resolution=res) as pcam:
		time.sleep(2)
		
		while True:
			img = np.empty((res[1], res[0], 3), dtype=np.uint8)
			pcam.capture(img, 'rgb')

			img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
			retval, buffer = cv.imencode('.jpg', img)
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route("/")
def home():
	return "Hello World! Welcome to PiPy Imaging API"

@app.route("/still", methods=['GET'])
def still():
	res_width = 640
	res_height = 480
	rotation_val = 0
	
	temp_res_width = request.args.get('width', default=-1, type=int)
	temp_res_height = request.args.get('height', default=-1, type=int)
	if temp_res_width > 0 and temp_res_height > 0:
	  res_width = temp_res_width
	  res_height = temp_res_height

	temp_rotation_val = request.args.get('rotate', default=-1, type=int)
	if temp_rotation_val > 0:
		rotation_val = temp_rotation_val

	with PiCamera(resolution=(res_width, res_height)) as pcam:
		# Set up the camera
		pcam.rotation = rotation_val

		time.sleep(2)
		img = np.empty((res_height, res_width, 3), dtype=np.uint8)
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
	return Response(livestream_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
