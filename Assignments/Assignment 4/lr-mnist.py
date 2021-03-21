#!/usr/bin/python

import sys
import os
import argparse
import pandas as pd
from pathlib import Path
sys.path.append(os.path.join(".."))
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets
from sklearn import metrics
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import utils.classifier_utils as clf_util

def main():
    # initialize argument parser
    ap = argparse.ArgumentParser(description="Train a logisitc regression on mnist dataset and print evaluation metrics")
    ap.add_argument('-p', '--path', default= Path('../data/'), type = Path, help="Path to the data")
    args = ap.parse_args()
             
    # If there the training and label csv files aren't in the data folder
    # then fetch the dataset from openml and save it to the defined outpaths
    data_path = os.path.join('..', 'data')

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

    img, label = load_mnist(data_path)
    print(sorted(set(label)))

    # We are assuming the min and max values for pixel intensities
    # are between 0 and 255. The minmax normalization from session 7
    # might give values between say 10 and 230, which might not work
    # well when given a new image that has pixel values above or below those
    img_scaled = img/255.0

    # make training and test-set
    img_train, img_test, label_train, label_test = train_test_split(img, 
                                                        label, 
                                                        random_state=9,
                                                        train_size=0.8, 
                                                        test_size=0.2)

    # Train the logistic model
    classifier = LogisticRegression(penalty='none', 
                             tol=0.1, 
                             solver='saga',
                             multi_class='multinomial').fit(img_train, label_train)


    # calculate the the label predictions for all img test data
    label_pred = classifier.predict(img_test)

    print(label_pred)

    # Calculate metrics of accuracy
    classification_metrics = metrics.classification_report(label_test, label_pred)

    print(classification_metrics)
                   
if __name__ == '__main__':
    main()

