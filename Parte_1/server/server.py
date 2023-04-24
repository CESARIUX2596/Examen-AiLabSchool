import sys
import os
import shutil
import time
import traceback

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib

app = Flask(__name__)

# inputs
training_data = '../data/healthcare-dataset-stroke-data.csv'


model_directory = '../models/RFC/'
model_file_name = '%s/finalized_model.sav' % model_directory


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # get the data
        data = request.get_json(force=True)

        # convert data into dataframe
        data.update((x, [y]) for x, y in data.items())
        data_df = pd.DataFrame.from_dict(data)

        # load the model
        model = joblib.load(model_file_name)

        # predictions
        result = model.predict(data_df)

        # send back to browser
        output = {'results': int(result[0])}

        # return data
        return jsonify(results=output)

    except:
        return jsonify({'trace': traceback.format_exc()})
