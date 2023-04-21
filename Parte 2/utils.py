import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import tensorflow as tf


class ProcessingUtils:
    @staticmethod
    def load_dataset(self, path, classes, img_size=(224, 224), shuffle=True, verbose=True):
        '''Load the dataset from the given path with folder for each class'''
        X = []
        y = []
        for i, cls in enumerate(classes):
            if verbose:
                print('Loading class', cls, '...')
            for img_name in os.listdir(path + cls):
                img = cv2.imread(path + cls + '/' + img_name)
                img = cv2.resize(img, img_size)
                X.append(img)
                y.append(i)
        if shuffle:
            X, y = self.shuffle_dataset(X, y)
        return np.array(X), np.array(y)

    @staticmethod
    def shuffle_dataset(self, X, y):
        c = list(zip(X, y))
        random.shuffle(c)
        X, y = zip(*c)
        return np.array(X), np.array(y)

    @staticmethod
    def plot_dataset(X, y, classes, n=10):
        plt.figure(figsize=(20, 10))
        for i in range(n):
            plt.subplot(2, n, i + 1)
            plt.imshow(X[i])
            plt.title(classes[y[i]])
            plt.axis('off')
        plt.show()

    @staticmethod
    def create_augmented_data_generator(self, X_train, y_train, batch_size=32):
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')
        datagen.fit(X_train)
        return datagen.flow(X_train, y_train, batch_size=batch_size)

    @staticmethod
    def train_pipeline(self, X_train, y_train, batch_size=64):
        datagen = self.create_augmented_data_generator(
            X_train, y_train, batch_size=batch_size)
        return datagen
