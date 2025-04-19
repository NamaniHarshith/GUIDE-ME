import numpy as np
import cv2
import mahotas
import joblib
import pickle

# Load the trained model and BOVW codebook
MODEL = MODEL = r'C:\model\API service\models\rfclassifier_600.sav'
BOVW = r'C:\model\API service\models\bovw_codebook_600.pickle'

# Hu Moments
def fd_hu_moments(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature

# Haralick Texture
def fd_haralick(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haralick = mahotas.features.haralick(gray).mean(axis=0)
    return haralick

# Color Histogram
def fd_histogram(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    bins = 8
    hist = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

# SIFT Bag of Visual Words
def feature_extract(im, bowDiction):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    feature = bowDiction.compute(gray, sift.detect(gray))
    return feature.squeeze()

# Preprocess the image and make a prediction
def predict_currency(image_path):
    # Load the trained model and input image
    loaded_model = joblib.load(MODEL)
    image = cv2.imread(image_path)

    # Resize the image
    IMG_SIZE = 320
    (height, width, channel) = image.shape
    resize_ratio = 1.0 * (IMG_SIZE / max(width, height))
    target_size = (int(resize_ratio * width), int(resize_ratio * height))
    input_image = cv2.resize(image, target_size)

    # Load the BOVW codebook
    pickle_in = open(BOVW, "rb")
    dictionary = pickle.load(pickle_in)

    # Initialize SIFT BOW image descriptor extractor
    sift2 = cv2.xfeatures2d.SIFT_create()
    bowDiction = cv2.BOWImgDescriptorExtractor(sift2, cv2.BFMatcher(cv2.NORM_L2))
    bowDiction.setVocabulary(dictionary)

    # Extract the features
    Hu = fd_hu_moments(input_image)
    Harl = fd_haralick(input_image)
    Hist = fd_histogram(input_image)
    Bovw = feature_extract(input_image, bowDiction)

    # Generate a feature vector by combining all features
    mfeature = np.hstack([Hu, Harl, Hist, Bovw])

    # Predict the output using the trained model
    output = loaded_model.predict(mfeature.reshape((1, -1)))

    # Class-label dictionary
    label = {0: "10", 1: "20", 2: "50", 3: "100", 4: "200", 5: "500", 6: "2000"}

    return str(label.get(output[0], "Unknown Denomination")+" rupees")
# from flask import Flask, request, jsonify
# import tensorflow as tf
# import numpy as np
# import cv2
# import os
# from werkzeug.utils import secure_filename

# # Initialize Flask app
# app = Flask(__name__)

# # Load the trained model (.h5)
# model = tf.keras.models.load_model(r"C:\model\API service\models\model_final_B8.h5")

# # Label mapping



# # Image preprocessing
# def preprocess_image(file_path):
#     image = cv2.imread(file_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = cv2.resize(image, (192, 192))  # Match training size
#     image = image.astype("float32") / 255.0
#     return np.expand_dims(image, axis=0)


# # Prediction endpoint
# @app.route('/predict', methods=['POST'])
# def predict_currency(image_path):
#     class_names = ['10', '20', '50', '100', '200', '500', '2000']
    
#     try:
#         img1 = preprocess_image(image_path)
#         pred = model.predict(img1)
#         predicted_class_index = np.argmax(pred)
        
#         if pred is None or len(pred) == 0:
#             predicted_label = "Unknown Denomination"
#         else:
#             predicted_label = class_names[predicted_class_index]
        
#         print(f"Predicted Class: {predicted_label}")

#         return {
#             'Predicted_Class': predicted_label
#         }

#     except Exception as e:
#         return {'error': str(e)}

# from PIL import Image
# import torch
# from model import ConvolutionalNetwork
# import torchvision.transforms as transforms
# from flask import Flask, request, jsonify

# class_names = ['10', '20', '50', '100', '200', '500', '2000']

# def load_model():
#     model = ConvolutionalNetwork()
#     model.load_state_dict(torch.load(r"C:\model\API service\models\model_final.pth"))
#     model.eval()
#     return model

# def preprocess_image(image_path):
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#     ])
#     image = Image.open(image_path).convert("RGB")
#     return transform(image).unsqueeze(0)




# def predict_currency( image_path):
#     model=load_model()
#     image = preprocess_image(image_path)
#     output = model(image)
#     predicted = torch.argmax(output, dim=1)
#     return str(class_names[predicted.item()]+"rupees")
