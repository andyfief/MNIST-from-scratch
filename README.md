# MNIST From Scratch

## scratchMNIST.org

A handwritten digit recognizer built from the ground up using **Python** and **NumPy**. No TensorFlow, no PyTorch — just math and code.

![MNIST Digits](https://upload.wikimedia.org/wikipedia/commons/2/27/MnistExamples.png)

---

# Description

This project implements a neural network from scratch to classify images from the MNIST dataset (28x28 grayscale images of handwritten digits). It's designed for learning purposes — to understand how neural networks work under the hood.

---

## Features

-  Feedforward neural network using only Python and NumPy, including backpropogation and gradient descent.
-  Trains on the official MNIST dataset
-  Accuracy tracking during training
-  React-based front end for a dynamic and responsive user interface that allows users to make predictions on their own drawn digits.

## Files

-  Training script: training_scripts/model.py
-  Saved model weights (if you don't want to train it yourself): models/model_weights.pkl
-  Data Visualization tool: auxillary/mnist_viewer.py
-  Converting ubyte files to CSV: auxillary/Convert_CSV.py
-  Preprocessing script: auxillary/cleanIMG.py
-  Raw MNIST ubyte files: MNIST_Data/*
-  React Components, Frontend JavaScript, CSS, HTML: webapp/frontend
-  Python API for live feed forward predictions: webapp/backend

---

# Installation

## 1. Clone the repository
```bash
git clone https://github.com/andyfief/MNIST-from-scratch.git
cd mnist-from-scratch
```
## 2. Install Dependencies
Install backend dependencies:
In the root directory,
```bash
pip install -r requirements.txt
```
Install frontend dependencies **(Only required if using the webapp)**:
```bash
cd ./webapp/frontend
npm install
```

# Usage
## 1 Converting Ubyte to CSV
CSV files are required. To convert ubyte files to CSV, use Convert_CSV.py:

Include the path to the ubyte files at the top of the script:
```bash
mnist_train_x = './MNIST_Data/train-images.idx3-ubyte'
mnist_train_y = './MNIST_Data/train-labels.idx1-ubyte'
mnist_test_x = './MNIST_Data/t10k-images.idx3-ubyte'
mnist_test_y = './MNIST_Data/t10k-labels.idx1-ubyte'
```
Include the output file path at the bottom of the script:
```bash
convert(mnist_train_x, mnist_train_y, './MNIST_Data/train.csv', 60000)
convert(mnist_test_x, mnist_test_y, 'MNIST_Data/test.csv', 10000)
```
In the auxillary directory:
```bash
python Convert_CSV.py
```

## 2 Preprocess the Data
While training the model on raw MNIST data is viable and reasonable, preprocessing the model results in a higher accuracy. 
When loading a model in the front end, it is highly recommended that the weights are learned on preprocessed data, as the same
preprocessing pipeline is used in the backend API.

Include input and output file paths at the bottom of CleanIMG.py:
```bash
process_all_rows("../MNIST_Data/test.csv", "../MNIST_Data/cleanTest.csv")
process_all_rows("../MNIST_Data/train.csv", "../MNIST_Data/cleanTrain.csv")
```
In the auxillary directory:
```bash
python CleanIMG.py
```

## Train the Model
Include input file paths for training and testing csv files at the top of model.py:
```bash
train_file = open('../MNIST_Data/cleanTrain.csv', 'r')
test_file = open('../MNIST_Data/cleanTest.csv', 'r')
```
In the training_scripts directory:
```bash
python model.py
```
Outputs are saved by default to models/model_weights.pkl. This output file can be changed:
```bash
def save_model_weights(model, outfile='../models/model_weights.pkl'):
```

## Using the webapp locally
Start the frontend:
```bash
cd ./webapp/frontend
npm run dev
```
Start the backend:
```bash
cd ./webapp/backend
python app.py
```
