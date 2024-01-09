import numpy as np
import os
import cv2
import base64
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template, Response, send_from_directory

app = Flask(__name__)

# Load the model
model = load_model("C:/Users/SRIYA CHINMAYEE/Desktop/ASL/IMAGE UPLOAD APPLICATION/asl_vgg16_best_weights.h5", compile=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    f = request.files['image']
    print("current path")
    basepath = os.path.dirname(__file__)
    print("current path", basepath)
    filepath = os.path.join(basepath, 'uploads', f.filename)
    print("upload folder is ", filepath)
    f.save(filepath)

    img = image.load_img(filepath, target_size=(64, 64))
    x = image.img_to_array(img)
    print(x)
    x = np.expand_dims(x, axis=0)
    print(x)
    y = model.predict(x)
    preds = np.argmax(y, axis=1)
    index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']
    text = "The ASL Sign is recognised as: " + str(index[preds[0]])
    return text

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/asl_vgg16_best_weights.h5')
def send_model():
    return send_from_directory('.', 'asl_vgg16_best_weights.h5')

if __name__ == '__main__':
    app.run(debug=False)
