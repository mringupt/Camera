from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, join_room, leave_room
from os import environ
import base64
import os
import json
import cv2
import numpy as np
app = Flask(__name__)

socketio = SocketIO(app, always_connect=True, engineio_logger=True)


@socketio.on('connect')
def connected():
    print("\n\nPyton Now i am connected\n\n")

@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('image-upload')
def imageUpload(image):
    print('Pthon:entering\n\n\n')
    str=image['binary']
    header, encoded = str.split(",", 1)
    data = base64.b64decode(encoded)
    filepath= os.path.join(app.config.root_path, 'static\\images\\sample.jpeg')

    with open(filepath, "wb") as f:
        f.write(data)
    img=cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filepath, gray)
    
    img_data=get_base64_encoded_image(filepath)
    print(img_data)
    socketio.emit("open_cv",img_data)

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')    

@app.route('/')
def index():
   return render_template(
        'index.html')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run(app,host=HOST,port=PORT)

