from flask import Flask, request, jsonify
import os
from currency_processing import predict_currency  # Import the function
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from flask import Flask, request
import numpy as np
import cv2
from PIL import Image
import io
import json
import os
import pytesseract

from twilio.rest import Client
from objdet import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# =========== SOS config ==========
AccountSID = os.getenv("TWILIO_SID")


app = Flask(__name__)
client = Client(AccountSID)


def sendMessage(client_num, message):
    client.messages.create(
        body=message,
        from_=+18148851848,
        to='+91' + client_num
    )


@app.route('/currency', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the image temporarily
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Predict using the uploaded image
        prediction = predict_currency(file_path)

        return prediction

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/detected_obj", methods=["POST"])
def obj_det():
    model_name = "yolov5s.onnx"
    net = build_model(yolo_path, model_name)
    image = request.files["file"].read()
    image = Image.open(io.BytesIO(image))
    npimg = np.array(image)
    image = npimg.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    labelsPath = "classes.txt"
    class_list = load_classes(labelsPath)

    inputImage = format_yolov5(image)
    res, laptop_widths = get_prediction(inputImage, net, class_list)
    if laptop_widths:
        res += ' at distance '
        ref_image = cv2.imread(os.path.join(path, "calibration", "Ref_image.png"))
        _, ref_image_laptop_width = get_prediction(ref_image, net, class_list)
        focal_length_found = focal_length_finder(Known_distance, Known_width, ref_image_laptop_width[0])
        for laptop_width in laptop_widths:
            distance = distance_finder(focal_length_found, Known_width, laptop_width)
        res = res + '{:.2f} centimeters'.format(distance)
    return res


@app.route("/sos", methods=["POST"])
def sos():
    numbers = json.loads(request.data)['data']
    for num in numbers:
        sendMessage(num, "SOS EMERGENCY FROM BLIND PERSON")
    return "Success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
