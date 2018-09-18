#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os as os
import numpy as np

# dataset settings
DATA_PATH = "../dataset/quickdraw_data_full/" # contains all .npz files
OUT_PATH = "../dataset/train_test_20k/"
INSTANCES_PER_CLASS = 20000 # total instances per class
TEST_SIZE = 0.2


# collect information about the dataset
# each file is a class
file_name_list = []
for (dirpath, dirnames, filenames) in os.walk(DATA_PATH):
    if filenames != '.DS_Store': # skip macOS files
        file_name_list.extend(filenames)
        break


# number of correct files is equal to number of classes 
num_classes = len(file_name_list)


# create directory if required
if not os.path.isdir(OUT_PATH + "train/"):
    os.makedirs(OUT_PATH + "train/")
if not os.path.isdir(OUT_PATH + "test/"):
    os.makedirs(OUT_PATH + "test/")


# now read each file, slice instances and devide the dataset in train and validation set 
for file_name in file_name_list:
    txt_path = DATA_PATH + file_name
    x = np.load(txt_path) # all images of one class

    # first shuffle the entire dataset
    np.random.seed(np.random.randint(1, 10e6))
    np.random.shuffle(x)

    # slice a big part
    x = x[:INSTANCES_PER_CLASS] 

    # create train and validation set
    limit = (int) (x.shape[0] * (1  - TEST_SIZE))
    x_train = x[: limit]
    x_test = x[limit :]

    print("train size class {} : {}".format(file_name, x_train.shape))
    print("test size class {}: {}".format(file_name, x_test.shape))

    np.save(OUT_PATH + "train/" + file_name, x_train)
    np.save(OUT_PATH + "test/" + file_name, x_test)


    
