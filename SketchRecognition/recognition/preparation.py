#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import os as os
import csv

import classification


def collect_data(num_classes_limit=None):
    """
    Preprocessing step: Collect information about the dataset and build train and test set.
    The files of the dataset should be splitted in train and test before.

    Args:
        num_classes_limit

    Returns:
        num_classes:    Number of valid classes
        x_train:    Images for train data
        x_test:    Images for test data
        y_train:    Indexes for train data
        y_test:  Indexes for test data
        classes_dict:   Dictionary for index class and class label

    """
    file_name_list = [] # collect all filenames / class files
    for (dirpath, dirnames, filenames) in os.walk(classification.DATA_PATH + "train/" ):
        if filenames != '.DS_Store':
            file_name_list.extend(filenames)
            break

    # potentially slice classes if a class limit is given
    if num_classes_limit != None:
        file_name_list = file_name_list[:num_classes_limit]

    # number of valid classes
    num_classes = len(file_name_list)

    # index and label connection
    classes_dict = {}
    for index, file_name in enumerate(file_name_list):
        # add class label
        label = file_name[:-4]
        classes_dict[index] = label
        print("read " + str(index + 1) + "/" + str(num_classes)+ " " + label)


    # given the dataset seperated in 80:20 for train and test data
    # able to select just a part
    test_size = int(classification.INSTANCES_PER_CLASS / 5)
    train_size = int(classification.INSTANCES_PER_CLASS - test_size)

    print("train size: {}".format(train_size))
    print("test size: {}".format(test_size))

    x_train, y_train = getData(classification.DATA_PATH + "train/", file_name_list, num_classes, train_size)
    print("dataset total train shape {}".format(x_train.shape))
    print("x_train size in byte: {}".format(x_train.nbytes))
    print("y_train size in byte: {}".format(y_train.nbytes))
    x_test, y_test = getData(classification.DATA_PATH + "test/", file_name_list, num_classes, test_size)
    print("dataset total test shape {}".format(x_test.shape))
    print("x_test size in byte: {}".format(x_test.nbytes))
    print("y_test size in byte: {}".format(y_test.nbytes))

    # store labels in seperate file
    with open(classification.MODEL_PATH + "labels.csv", 'w') as f:
        writer = csv.writer(f)
        for key, value in classes_dict.items():
            writer.writerow([key, value])

    return num_classes, x_train, x_test, y_train, y_test, classes_dict

def getData(path, file_name_list, num_classes, instances_slice):
    """
    Returns a shuffled set of images and a set of related labels.

    Args:
        path:   Path that contains the data e.g. "./train/"
        file_name_list:      List of all valid filenames
        number_of_classes:    Number of all classes but equal to len(file_name_list)
        instances_slice:    Number of instances to keep

    Returns:
        xtotal: The shuffled set of all images
        ytotal: The related indexes
    """


    for index, file_name in enumerate(file_name_list):
        x = np.load(path + file_name) # load all images
        x = x.astype('float16') / 255. # scale images
        y = [index] * len(x) # all classes as list

        print("{} : slice".format(index))
        x = x[:instances_slice]
        y = y[:instances_slice]

        # if list is empty allocate enough memory
        if index == 0:
            xtotal = np.empty([num_classes, len(x), classification.IMG_SIZE ])
            ytotal = np.empty([num_classes, len(x)])

        xtotal[index] = x
        ytotal[index] = y

        print(x.shape)

    # number of classes * number of instances, image size
    xtotal = xtotal.reshape(xtotal.shape[0] * xtotal.shape[1], classification.IMG_SIZE)
    ytotal = ytotal.flatten()

    # reshape to 28x28x1 grayscale image
    xtotal = xtotal.reshape(xtotal.shape[0], classification.IMG_WIDTH, classification.IMG_HEIGHT, classification.IMG_DIM)

    return xtotal, ytotal
