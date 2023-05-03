import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dropout,
    BatchNormalization,
)
import numpy as np
import h5py


# Create convolution blocks
class ConvBlock(tf.keras.layers.Layer):
    def __init__(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        pool_size,
        pool_strides,
        pool_padding,
        activation,
        name=None,
        **kwargs
    ):
        super(ConvBlock, self).__init__(name=name, **kwargs)
        self.conv = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            activation=activation,
        )
        self.pool = MaxPooling2D(
            pool_size=pool_size, strides=pool_strides, padding=pool_padding
        )
        self.batch_norm = BatchNormalization()

    def call(self, inputs):
        x = self.conv(inputs)
        x = self.pool(x)
        x = self.batch_norm(x)
        return x

    def get_config(self):
        config = super(ConvBlock, self).get_config()
        config.update(
            {"conv": self.conv, "pool": self.pool, "batch_norm": self.batch_norm}
        )
        return config


best_params = {
    "batch_size": 64,
    "conv1_filters": 64,
    "conv2_filters": 64,
    "conv3_filters": 256,
    "conv4_filters": 64,
    "dense": 512,
    "dropout": 0.8906428588508701,
    "epochs": 100,
    "learning_rate": 0.001,
}


def build_model():
    best_model = Sequential(
        [
            ConvBlock(
                filters=best_params["conv1_filters"],
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                pool_size=(2, 2),
                pool_strides=(2, 2),
                pool_padding="valid",
                activation="relu",
                name="conv_block_1",
            ),
            ConvBlock(
                filters=best_params["conv2_filters"],
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                pool_size=(2, 2),
                pool_strides=(2, 2),
                pool_padding="valid",
                activation="relu",
                name="conv_block_2",
            ),
            ConvBlock(
                filters=best_params["conv3_filters"],
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                pool_size=(2, 2),
                pool_strides=(2, 2),
                pool_padding="valid",
                activation="relu",
                name="conv_block_3",
            ),
            ConvBlock(
                filters=best_params["conv4_filters"],
                kernel_size=(3, 3),
                strides=(1, 1),
                padding="same",
                pool_size=(2, 2),
                pool_strides=(2, 2),
                pool_padding="valid",
                activation="relu",
                name="conv_block_4",
            ),
            Dropout(best_params["dropout"]),
            Flatten(),
            Dense(best_params["dense"], activation="relu"),
            Dense(6, activation="sigmoid"),
        ]
    )

    # Generate a sample image and pass it through the model to generate variables
    sample_image = np.random.rand(1, 150, 150, 3)

    best_model(sample_image)
    best_model.load_weights(
        "D://Develop//Repos//Examen-AiLabSchool//Parte_2//models//20230502-212242_best_model_weights.h5"
    )
    best_model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return best_model
