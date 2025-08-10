from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Load the trained model once when the app starts
model_path = os.path.join(os.path.dirname(__file__), 'models', 'depression2_model_improved_cnn.keras')
model = tf.keras.models.load_model(model_path)

def predict_image(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)[0][0]

    # Flip logic: higher prediction means depression now
    if prediction >= 0.6:
        label = "No Depression"
        description = ""
    elif prediction >= 0.3:
        label = "Mild Depression"
        description = f"Depression Level: {prediction * 100:.2f}% (Mild)"
    else:
        label = "High Depression"
        description = f"Depression Level: {prediction * 1000:.2f}% (High)"

    return {"result": label, "details": description}


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        result = predict_image(file_path)
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # clean up

    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Depression Detection API! Use POST /predict with an image file."

if __name__ == '__main__':
    app.run(debug=True)
