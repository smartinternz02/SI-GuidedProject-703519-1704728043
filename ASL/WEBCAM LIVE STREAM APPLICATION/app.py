# app.py
# working
from flask import Flask, render_template, request
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from flask_socketio import SocketIO
import base64
import os

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']
model = load_model("C:/Users/SRIYA CHINMAYEE/Desktop/ASL/WEBCAM LIVE STREAM APPLICATION/asl_vgg16_best_weights.h5")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify(image):
    if image.shape[2] == 3:
        # The image is already in BGR format
        img = image
    else:
        # Convert the grayscale image to BGR
        img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    img = cv2.resize(img, (64, 64))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    proba = model.predict(img)
    idx = np.argmax(proba)
    confidence_score = proba[0][idx] * 100
    if 0 <= idx < len(alphabet):
        return alphabet[idx], confidence_score
    else:
        return "Invalid index", confidence_score  # Handle the case where the index is out of range


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(frame):
    nparr = np.fromstring(base64.b64decode(frame.split(',')[1]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    alpha, confidence = classify(img)
    socketio.emit('classification_result', {'alpha': alpha, 'confidence': confidence})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Use Gunicorn to run the app
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)  # Disable the Flask reloader
