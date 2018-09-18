import numpy as np
import itertools
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import matplotlib.ticker as ticker
import os

#from recognition import classification
import classification
from keras.utils import np_utils


def plot_training_history_accuracy(hist):
    """
    Plots the training history of a keras model using matplotlib and saves as image to training_process.png.
    Saves the image to MODEL_PATH specified in classification.py.

    Args:
        hist: The Keras model

    Returns:
        None: Simple writes result to file    
    """
    plt.clf()
    plt.plot(hist.history['acc'])
    plt.plot(hist.history['val_acc'])
    plt.title('model accuracy during training')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(classification.MODEL_PATH + "training_process.png")


def plot_confusion_matrix(pred, test, classes):
    """
    Plots a confusion matrix and saves to file (.csv and .png).
    Saves the image to MODEL_PATH specified in classification.py.

    Args:
        pred:   Output prediction vector
        test:   List of binary label vectors for each class e.g. [[0,0,1,..],[0,1,0,..], ...]
        classes: List of class labels

    Returns:
        None:   Simple writes results to file
    """

    figsize = (10,10) # manually set the figure size depending on matrix size

    fig = plt.figure(figsize=figsize)
    # perform argmax to get class index to get a list of indexes [0,1,2,0,2,2,....]
    pred_classes = pred.argmax(axis=-1)
    test_classes = test.argmax(axis=-1)
    # convert class index to class label for confusion matrix
    pred_classes = list(map(lambda i: classes[i], pred_classes))
    test_classes = list(map(lambda i: classes[i], test_classes))

    # create the confusion matrix
    cm = confusion_matrix(pred_classes, test_classes, labels=classes)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    

    fmt = '.2f'
    thresh = cm.max() / 2.

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if (format(cm[i, j], fmt) == '0.00'):
            item = '0'
        else:
            item = format(cm[i, j], fmt)
        plt.text(j, i, item,
            horizontalalignment="center",
            color="white" if cm[i, j] < thresh else "black")

    ax = fig.add_subplot(111)
    ax.set_xticklabels([''] + classes, rotation=45)
    ax.set_yticklabels([''] + classes)
    plt.imshow(cm, aspect='auto', cmap=plt.get_cmap("viridis"))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    #plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # save result to file
    np.savetxt(classification.MODEL_PATH + "confusion_matrix.csv", cm, delimiter=",")
    plt.savefig(classification.MODEL_PATH + "confusion_matrix.png")
    


def plot_first_n_images(data, classes, classes_dict, n):
    """
    Plots the first n pictures and saves the images to MODEL_PATH specified in classification.py.

    Args:
        data:   The images as vector
        classes:   The class indexes of the images
        classes_dict: The dictionary for index - label connection
        n: Total number of images

    Returns:
        None:   Simple writes results to MODEL_PATH/imgs/
    """
    if not os.path.isdir(classification.MODEL_PATH + "imgs/"):
        os.makedirs(classification.MODEL_PATH + "imgs/")
    for k in range(n):
        plt.figure()
        plt.clf()
        plt.imshow(data[k].reshape(classification.IMG_WIDTH, classification.IMG_HEIGHT))
        plt.gray()
        plt.savefig(classification.MODEL_PATH + "imgs/" + classes_dict[classes[k]] + "-" + str(k) + ".png")


# just a  playground to test functionality
if __name__ == "__main__":
    import os
    print(os.getcwd())
    if not os.path.isdir(classification.MODEL_PATH):
        os.makedirs(classification.MODEL_PATH)

    num_classes = 20
    pred_random = np.random.randint(0, num_classes, size=1000)
    test_random = np.random.randint(0, num_classes, size=1000)
    classes_test = np.arange(num_classes).tolist()

    pred_random = np_utils.to_categorical(pred_random, num_classes=num_classes)
    test_random = np_utils.to_categorical(test_random, num_classes=num_classes)

    #plot_confusion_matrix(pred_random, test_random, classes_test)

    pred_classes = pred_random.argmax(axis=-1) 
    test_classes = test_random.argmax(axis=-1)
    # convert class index to class label for confusion matrix
    pred_classes = list(map(lambda i: classes_test[i], pred_classes))
    test_classes = list(map(lambda i: classes_test[i], test_classes))


    cm = confusion_matrix(pred_classes, test_classes, labels=classes_test)
    #cm = cm.astype('float')
    np.savetxt("confusion_matrix.csv", cm, delimiter=",")


