import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
import random
import tensorflow as tf


class ProcessingUtils:
    @staticmethod
    def load_dataset(
        path, classes, img_size=(224, 224), shuffle=True, seed=None, verbose=True
    ):
        """Load the dataset from the given path with folder for each class"""
        X = []
        y = []
        for i, cls in enumerate(classes):
            if verbose:
                print("Loading class", cls, "...")
            for img_name in os.listdir(path + cls):
                img = cv2.imread(path + cls + "/" + img_name)
                img = cv2.resize(img, img_size)
                X.append(img)
                y.append(i)
        if shuffle:
            if seed != None:
                X, y = ProcessingUtils.shuffle_dataset(X, y, seed)
            else:
                X, y = ProcessingUtils.shuffle_dataset(X, y)
        return np.array(X), np.array(y)

    @staticmethod
    def shuffle_dataset(X, y, seed=None):
        """Shuffle the dataset"""
        c = list(zip(X, y))
        if seed != None:
            random.Random(seed).shuffle(c)
        else:
            random.shuffle(c)
        X, y = zip(*c)
        return np.array(X), np.array(y)

    @staticmethod
    def sample_dataset(X, y, class_dict, n=5):
        """Plot a sample of the datasetwith n images per class, default 5 images per class"""
        fig, axs = plt.subplots(len(np.unique(y)), n, figsize=(15, 15))
        for i, cls in enumerate(np.unique(y)):
            for j in range(n):
                img = cv2.cvtColor(X[y == cls][j], cv2.COLOR_BGR2RGB)
                axs[i, j].imshow(img)
                cls_name = class_dict[cls]
                axs[i, j].set_title(cls_name)
                axs[i, j].axis("off")
        plt.show()

    @staticmethod
    def normalize_data(X):
        """Normalize the dataset"""
        return X / 255.0

    @staticmethod
    def reshape_data(X):
        """Reshape images to be used in the model"""
        return X.reshape(-1, 150, 150, 3)

    @staticmethod
    def rgb2bgr(X):
        """Convert RGB images to BGR"""
        return cv2.cvtColor(X, cv2.COLOR_RGB2BGR)

    @staticmethod
    def json2numpy(json):
        """Convert image in json to numpy array"""
        img = np.fromstring(json, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        img = img.fromarray(img.astype("uint8"))

    @staticmethod
    def split_data(X, y, train_size, test_size, val_size=None, seed=None):
        # Split data into train and test sets while maintaining class proportions
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            train_size=train_size + val_size,
            test_size=test_size,
            stratify=y,
            random_state=seed,
        )

        # Split train set into train and validation sets if val_size is given
        if val_size is not None:
            X_train, X_val, y_train, y_val = train_test_split(
                X_train,
                y_train,
                train_size=train_size / (train_size + val_size),
                test_size=val_size / (train_size + val_size),
                stratify=y_train,
                random_state=seed,
            )
            return X_train, X_test, X_val, y_train, y_test, y_val
        else:
            return X_train, X_test, y_train, y_test

    @staticmethod
    def create_data_generator(X_train, y_train, batch_size=64):
        datagen = tf.keras.preprocessing.image.ImageDataGenerator()
        datagen.fit(X_train)
        return datagen.flow(X_train, y_train, batch_size=batch_size)

    @staticmethod
    def create_augmented_data_generator(X_train, y_train, batch_size=64):
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode="nearest",
        )
        datagen.fit(X_train)
        return datagen.flow(X_train, y_train, batch_size=batch_size)

    @staticmethod
    def train_pipeline(X_train, y_train, batch_size=64):
        datagen = ProcessingUtils.create_augmented_data_generator(
            X_train, y_train, batch_size=batch_size
        )
        return datagen
