from utils import ProcessingUtils
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import numpy as np
from model import build_model
import cv2

app = Flask(__name__)
CORS(app)

# generate and compile model
model = build_model()


# Create the API endpoint to predict
@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    # Get the img from the request body
    img_file = request.files.get("img")
    if not img_file:
        return jsonify({"error": "Missing image file"}), 400
    img_bytes = img_file.read()
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = ProcessingUtils.reshape_data(img)
    img = ProcessingUtils.normalize_data(img)
    pred = np.argmax(model.predict(img), axis=-1)
    return jsonify({"Prediction": str(pred[0])})
    # return jsonify({"Prediction": 1})


@app.route("/ping")
def ping():
    return "Pong!"


if __name__ == "__main__":
    app.run(debug=True)
