#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


def build_model(input_shape, num_classes):
    """
    Builds the model architecture based on MNIST CNN
    https://www.tensorflow.org/tutorials/estimators/cnn

    Args:
        input_spape: Input shape of the model
        num_classes: Number of classes

    Returns:
        keras.models.Model: The created model

    """

    inputs = Input(shape=input_shape)
    x = Conv2D(32, (5,5), activation='relu')(inputs)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(0.2)(x)
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    return Model(inputs=inputs, outputs=predictions)
