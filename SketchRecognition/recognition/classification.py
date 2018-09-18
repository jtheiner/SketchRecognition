#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os as os
from keras.models import load_model
from keras.utils import np_utils

import model as md
import preparation as prep
import visualization as vis
from keras import metrics

# ----------- dataset settings -----------

# number of instances per class used for train and test in total:
# should be smaller or equal than generated subset
INSTANCES_PER_CLASS = 5000
NUM_CLASS_LIMIT = 345 # limit of classes
# path of the dataset seperated in train and test
DATA_PATH = os.path.join(os.getcwd(), "../dataset/train_test_20k/")
# path for all created files
MODEL_PATH = os.path.join(os.getcwd(), "models/" + str(NUM_CLASS_LIMIT) + "/" + str(INSTANCES_PER_CLASS) + "/")

# ----------- model settings -----------

MODEL_NAME = 'model.h5' # name for the freezed model
# input size
IMG_WIDTH = 28
IMG_HEIGHT = 28
IMG_SIZE = IMG_WIDTH * IMG_HEIGHT
IMG_DIM = 1

# training settings
EPOCHS = 10
BATCH_SIZE = 256


def top_3_acc(y_true, y_pred):
    return metrics.top_k_categorical_accuracy(y_true, y_pred, k=3)

if __name__ == "__main__":

    # create new directories if required
    if not os.path.isdir(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    # get the dataset
    num_classes, x_train, x_test, y_train, y_test, classes_dict = prep.collect_data(NUM_CLASS_LIMIT)
    print("trainingsset instances {}".format(x_train.shape))
    print("trainingsset labels {}".format(y_train.shape))

    # plot first test images
    #vis.plot_first_n_images(x_test, y_test, classes_dict, 100)


    # class representation as "binary" vector
    y_train = np_utils.to_categorical(y_train, num_classes=num_classes)
    y_test = np_utils.to_categorical(y_test, num_classes=num_classes)

    # create or load keras model
    if not os.path.isfile(MODEL_PATH + MODEL_NAME):
        print("create model...")
        model = md.build_model(input_shape=x_train.shape[1:], num_classes=num_classes)
    else:
        print("load existing model...")
        model = load_model(MODEL_PATH +  MODEL_NAME, custom_objects={"top_3_acc": top_3_acc})

        # score trained model using validation set
        scores = model.evaluate(x_test, y_test, verbose=1)
        print('test loss:', scores[0])
        print('test accuracy:', scores[1])


    model.compile(loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy', top_3_acc])

    # print model information if desired
    print(model.summary())

    # model training from scratch or retrain by existing model
    hist = model.fit(x_train, y_train, batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=[x_test, y_test],
                    shuffle=True)


    #from keras.utils import plot_model
    #plot_model(model, to_file=MODEL_PATH + 'model.png')

    # evaluation process
    print("evaluate model...")

    # summarize history during training phase
    # plot training and validation set accuracy
    vis.plot_training_history_accuracy(hist)

    # test set evaluation

    scores = model.evaluate(x_test, y_test, verbose=1)
    print(scores)
    print('test loss:', scores[0])
    print('test accuracy:', scores[1])

    # create and plot confusion matrix
    #y_pred = model.predict(x_test)
    #vis.plot_confusion_matrix(y_pred, y_test, classes=list(classes_dict.values()))


    # freeze the model (architecture and weights)
    model.save(os.path.join(MODEL_PATH, MODEL_NAME))
    print('saved trained model at  {}'.format(os.path.join(MODEL_PATH, MODEL_NAME)))
