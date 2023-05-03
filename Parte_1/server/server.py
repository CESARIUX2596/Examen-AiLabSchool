import pickle

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib

app = Flask(__name__)

# read the model with pickle
filename = "./models/RFC/finalized_model.sav"
RFC_model = pickle.load(open(filename, "rb"))


# function to clean the data
def clean_data(data):
    # Data comes as a json, so we need to convert it to a dataframe
    data = pd.DataFrame(data)
    # Drop the columns that we don't need
    data = data.drop(["id", "Unnamed: 0", "Unnamed: 0.1", "Unnamed: 0.1.1"], axis=1)


# Create the API endpoint to predict
@app.route("/predict", methods=["POST"])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    # Make prediction using model loaded from disk as per the data.
    prediction = RFC_model.predict(pd.DataFrame(data))
    # Take the first value of prediction
    output = prediction[0]
    return jsonify(output)
