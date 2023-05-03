# Script file to create csv with train and test data
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle


# load the data
df = pd.read_csv(
    "D:\Develop\Repos\Examen-AiLabSchool\Parte_1\data\healthcare-dataset-stroke-data.csv"
)

# Encode categorical features
le = LabelEncoder()
text_data_features = [
    "gender",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status",
]
l3 = []
l4 = []
print("Label Encoder Transformation")
for i in text_data_features:
    df[i] = le.fit_transform(df[i])
    l3.append(list(df[i].unique()))
    l4.append(list(le.inverse_transform(df[i].unique())))
    print(i, " : ", df[i].unique(), " = ", le.inverse_transform(df[i].unique()))
print("Label Encoder Transformation Completed")

# Treat missing values, # Replace missing values with mean
df["bmi"].fillna(df["bmi"].mean(), inplace=True)

# Remove outliers
df = df[df["bmi"] < 50]

# Split the data into train and test maintaining the same distribution of the target variable
X = df.drop("stroke", axis=1)
y = df["stroke"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1313, stratify=y
)


# Save the train and test data to csv
X_train.to_csv("train.csv", index=False)
X_test.to_csv("test.csv", index=False)
y_train.to_csv("train_target.csv", index=False)
y_test.to_csv("test_target.csv", index=False)
