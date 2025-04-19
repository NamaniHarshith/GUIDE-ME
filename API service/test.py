import tensorflow as tf
import cv2
import numpy as np
def preprocess_image(file_path):
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (192, 192))  # Match training size
    image = image.astype("float32") / 255.0
    return np.expand_dims(image, axis=0)


class_names = ['10', '20', '50', '100', '200', '500', '2000']

model = tf.keras.models.load_model(r"C:\model\API service\models\model_final_B8.h5")
image=r"C:\Indian-Currency-Recognition-System-master\data\100\155_cb.png"
img1=preprocess_image(image)
pred = model.predict(img1)
predicted_class = np.argmax(pred)
print(f"Predicted Class: {class_names[predicted_class]}")
