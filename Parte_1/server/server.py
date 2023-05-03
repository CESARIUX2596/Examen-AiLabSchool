import pickle
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
cors = CORS(app)

# read the model with pickle
filename = "../models/RFC/finalized_model.sav"
RFC_model = pickle.load(open(filename, "rb"))


# function to clean the data
def clean_data(data):
    data = dict(data)
    data = pd.DataFrame.from_dict(
        [data],
    )
    data = data.drop(["id"], axis=1)
    return data


# Create the API endpoint to predict
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Convert json to dict
    data = clean_data(data)
    # Make prediction
    prediction = RFC_model.predict(data)
    print(prediction)
    # Return prediction
    # if prediction[0] == 1:
    #     return jsonify({"Prediction": "Stroke"})
    # else:
    #     return jsonify({"Prediction": "No Stroke"})
    return jsonify({"Prediction": str(prediction[0])})


@app.route("/ping")
def ping():
    return "Pong!"


if __name__ == "__main__":
    app.run(debug=True)
