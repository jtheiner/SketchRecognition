# Sketch Recognition
This repository contains a Keras model for Google's quickdraw dataset to classify sketches, an Android app for demonstration  
and describes the whole workflow to integrate a custom model to an Android app applaying [Tensorflow Lite][4]

#### Global project structure:

* "Android" folder:    Includes the Android Studio Project of the SketchRecognition App  
 * "SketchRecognition" folder:    Directory for the complete recognition task  
* "ModelTransform" folder:    Scripts for model conversion (Keras -> Tensorflow -> TFLite)  


# Dataset
I used a subset from Google's quickdraw dataset (see [Quick, draw!][1]) which contains more than 50 million drawings across 345 categories.
For this project I used the simplified drawings stored in Numpy bitmaps. These bitmaps contain 28x28 grayscale images.

# Model
I used a CNN architecture presented by [Tensorflow's MNIST tutorial][2] with a few modifications.

# Results of sketch recognition:

\# classes | \# training data | \# test data | top-1 accuracy | top-3 accuracy
---------- | ---------- | ---------- | ---------- | ----------
20 | 8000 | 2000 | 89.76% | 95.34%
345 | 4000 | 1000 | 65.57% | 82.71% 

The much higher top-3 accuracy using 345 classes is justified by the fact that there are some quite similar classes inside the dataset.

###### Confusion matrix for 20 classes:
<img src="/SketchRecognition/recognition/models/20/10000//confusion_matrix.png" width="800">

# To reproduce the presented results use this instruction

#### Structure of "SketchRecognition"
The directory "dataset" contains the data and all its subsets.
"preparation_helper" contains Python and Shell scripts for preprocessing steps
like dataset download, dataset instances reduction and dataset split in train and test set.
"recognition" is the python project for the classification task. Besides it contains a "models" directory
for all generated results (training process, images, frozen model, list of labels).

#### How to prepare the dataset:
1. Download the full dataset (ca. 40GB) via script or download a subset manually ([Link][5])
and put the files into the "dataset" directory.

2. Adapt the parameters in "split_train_test.py" to setup the directories, to reduce
the number of instances per class you want to keep and split the dataset in train and test data. Then run the script.

#### Full sketch recognition task:
The "classification.py" script contains model training, visualisation and evaluation. Before run, adapt the dataset path.
The main function describes the complete workflow from preprocessing over the model training to the evaluation. So feel free to make changes. Again, you can decide how many instances you want to use for training and test in total.


#### System Environment used for this task:
Ubuntu 18.04  
Python 3.6.5 with Anaconda  
Keras version 2.2.0  
Tensorflow version 1.8.0  

# Android App
<img src="/Android/app.png" width="250">

## The Model Conversion and Integration Task
#### How to convert the frozen Keras model to Tensorflow Lite:
1. Convert generated Keras model (*.h5) to tensorflow frozed graph (*.pb).
Run the nice script "keras_to_tensorflow.py" written by Amir H. Abdi (see [Repo][3]), but before specify parameters like input and output file names.
2. Take the generated tensorflow model (*.pb) and convert it to tensorflow lite using toco. You can run the "toco.sh" script.
Important note: Use the correct input and output array names and also the correct input shape size.
To inspect and verify these settings you can modify and run "pb_view.py" which loads the frozen tensorflow graph (*.pb).

#### How to integrate into the Android App:
Take the generated Tensorflow Lite model (.tflite) and the related "labels.csv" which were generated in the training task and move it to androids "assets" directory.

#### System Environment:
macOS High Sierra v. 10.13.6  
Android Studio 3.1.3  
Python 3.6.3 with Anaconda  
Keras 2.1.6  
Tensorflow 1.7.0 (For model conversion Tensorflow 1.7 is required!)  


[1]: https://github.com/googlecreativelab/quickdraw-dataset
[2]: https://www.tensorflow.org/tutorials/estimators/cnn
[3]: https://github.com/amir-abdi/keras_to_tensorflow
[4]: https://www.tensorflow.org/mobile/tflite/
[5]: https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/numpy_bitmap

