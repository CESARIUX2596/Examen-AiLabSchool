from utils import ProcessingUtils
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import numpy as np
from model import build_model

app = Flask(__name__)
cors = CORS(app)

# generate and compile model
model = build_model()


# Create the API endpoint to predict
@app.route("/predict", methods=["POST"])
def predict():
    # get the image from the request
    img = request.files["image"]
    # convert the image to a numpy array
    img = ProcessingUtils.json2numpy(img)
    img = ProcessingUtils.reshape_data(img)
    img = ProcessingUtils.rgb2bgr(img)
    img = ProcessingUtils.normalize_data(img)
    # make the prediction
    pred = np.argmax(model.predict(img), axis=-1)
    # return the prediction
    return jsonify({"class": pred[0]})


@app.route("/ping")
def ping():
    return "Pong!"


if __name__ == "__main__":
    app.run(debug=True)
