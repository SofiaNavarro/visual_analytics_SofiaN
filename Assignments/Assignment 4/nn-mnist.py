#!/usr/bin/python

import sys
import os
import argparse
import pandas as pd
from pathlib import Path
sys.path.append(os.path.join(".."))
from utils.neuralnetwork import NeuralNetwork
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.datasets import fetch_openml
from sklearn.metrics import accuracy_score
import numpy as np
import utils.classifier_utils as clf_util

def main():
    # initialize argument parser
    ap = argparse.ArgumentParser(description="Train a neural network classifier and print the evaluations metrics")
    ap.add_argument('-p', '--path', default= Path('../data/'), type = Path, help="Path to the data")
    ap.add_argument("-e", "--epochs", default=10, type = int, help = "numbers of epochs to train")
    args = ap.parse_args()
  
             
    # If there the training and label csv files aren't in the data folder
    # then fetch the dataset from openml and save it to the defined outpaths
    def load_mnist(data_path):
        img_path = os.path.join(data_path, 'mnist_img.csv')
        label_path = os.path.join(data_path, 'mnist_label.csv')
        if os.path.isfile(img_path) and os.path.isfile(label_path):
            img = pd.read_csv(img_path)
            label = pd.read_csv(label_path).squeeze() # Squeezes DataFrame into Series
        else:
            if not os.path.isdir(data_path):
                os.mkdir(data_path)
            img, label = fetch_openml('mnist_784', version=1, return_X_y=True)
            img.to_csv(img_path, sep=',', encoding='utf-8', index=False)
            label.to_csv(label_path, sep=',', encoding='utf-8', index=False)
        # convert to numpy array
        return (np.array(img), np.array(label))

    img, label = load_mnist(args.path)
    print(sorted(set(label)))

    # We are assuming the min and max values for pixel intensities
    # are between 0 and 255. The minmax normalization from session 7
    # might give values between say 10 and 230, which might not work
    # well when given a new image that has pixel values above or below those
    img_scaled = img/255.0

    # make training and test-set
    img_train, img_test, label_train, label_test = train_test_split(img,
                                                   label,
                                                   random_state = 9,
                                                   train_size = 0.8,
                                                   test_size=0.2)

    # convert the labels to a binary representation
    # so that the computer can map between 0 an 1
    # a way of taking our labels
    # creating a binary representation and feed that into the model
    # rather than the names of the labels themselves
    label_train = LabelBinarizer().fit_transform(label_train)
    label_test = LabelBinarizer().fit_transform(label_test)

    # train network
    print("[INFO] training network..")
    # the first layer is the input layer (size of the data) this case 64
    # then the size of the first hidden layer, then the second layer
    # and lastly the size of the output layer in this case 10 (there are 10 digits)
    neural_network = NeuralNetwork([img_train.shape[1], 32, 16, 10])
    print(f"[INFO] {neural_network}")
    neural_network.fit(img_train, label_train, epochs= args.epochs)
    
    # Evaluate network
    print(["INFO] evaluating network.."])
    predictions = neural_network.predict(img_test)
    predictions = predictions.argmax(axis=1)
    print(classification_report(label_test.argmax(axis=1), predictions))
                   
if __name__ == '__main__':
    main()