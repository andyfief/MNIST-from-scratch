# Currently Broken ASF

import matplotlib.pyplot as plt
import time
import numpy as np

train_file = open('./MNIST_Data/train.csv', 'r')
train_list = train_file.readlines()
train_file.close()

test_file = open('./MNIST_Data/test.csv', 'r')
test_list = test_file.readlines()
test_file.close()

print(len(train_list))
print(len(test_list))

class DNN:
    def __init__(self, sizes=[784, 128, 64, 10], epochs=10, lr=0.001):
        self.sizes = sizes
        self.epochs = epochs
        self.lr = lr

        input_layer = sizes[0]
        hidden_1 = sizes[1]
        hidden_2 = sizes[2]
        output_layer = sizes[3]

        self.params = {
            # Weight Matrices, linking layers and scale the variance
            #The order here is inversed from model1 using softmax (He initialization)
            'W1': np.random.randn(hidden_1, input_layer) * np.sqrt(2./input_layer),  # 128 x 784
            'W2': np.random.randn(hidden_2, hidden_1) * np.sqrt(2./hidden_1),        # 64 x 128
            'W3': np.random.randn(output_layer, hidden_2) * np.sqrt(2./hidden_2)     # 10 x 64
        }

    # sets values to be between 0 and 1
    # Not used in this ReLU implementation
    def sigmoid(self, x, derivative=False):
        if derivative:
            return (np.exp(-x))/((np.exp(-x)+1)**2)
        return 1/(1+np.exp(-x))
    
    # For the output layer
    # Converts scores to probabilities, and all outputs sum to 1
    def softmax(self, x):
        exps = np.exp(x-x.max())
        return exps / np.sum(exps, axis = 0)
    
    def ReLU(self, x, derivative=False):
        if derivative:
            return np.where(x > 0, 1.0, 0.0)
        return np.maximum(0, x)

    def forward_pass(self, x_train):
        params = self.params

        # take inputs from previous layer
        # compute weighted sum Z = W*A using dot product
        # apply activation function to get output A = activation(Z)

        params['A0'] = x_train # 784 x 1

        # input layer to hidden_1
        params['Z1'] = np.dot(params['W1'], params['A0']) # 128 x 1
        params['A1'] = self.ReLU(params['Z1'])

        # hidden1 to hidden2
        params['Z2'] = np.dot(params['W2'], params['A1'])
        params['A2'] = self.ReLU(params['Z2'])

        # hidden2 to output
        params['Z3'] = np.dot(params['W3'], params['A2'])
        params['A3'] = self.softmax(params['Z3'])

        return params['A3']
    
    # gradient descent
    def update_weights(self, change_w):
        for key, val in change_w.items():
            self.params[key] -= self.lr * val  # W_t+1 = W_t - lr*Delta_W_t

    def backward_pass(self, y_train, output):
        params = self.params

        change_w = {}

        # calculate W3 updat
            # calculates error at output layer derivative of loss function
            # multiplies gradient opf softmax to get gradient with respect to Z3
            # Uses outer product with activations from previous layer to get weight gradients
        error = output - y_train
        change_w['W3'] = np.outer(error, params['A2'])

        # calculate W2 update
            # Propogates error backward by multiplying by transpose of W3
            # Multiplies by derivative of sigmoid to get gradient with respect to Z2
            # Uses outer product to get weight gradients
        error = np.dot(params['W3'].T, error) * self.ReLU(params['Z2'], derivative=True)
        change_w['W2'] = np.outer(error, params['A1'])

        # calculate W1 update
        error = np.dot(params['W2'].T, error) * self.ReLU(params['Z1'], derivative=True)
        change_w['W1'] = np.outer(error, params['A0'])

        return change_w

    def compute_accuracy(self, test_data):
        predictions = []
        for x in test_data:
            values = x.split(",")
            inputs = (np.asarray(values[1:], dtype=float) / 255.0)
            targets = np.zeros(10) + 0.01
            targets[int(values[0])] = 0.99
            output = self.forward_pass(inputs)
            pred = np.argmax(output)
            predictions.append(pred==np.argmax(targets))

        return np.mean(predictions)

    def train(self, train_list, test_list):
        start_time = time.time()
        for i in range(self.epochs):
            for x in train_list:
                values = x.split(",")
                inputs = (np.asarray(values[1:], dtype=float) / 255.0)
                targets = np.zeros(10) + 0.01
                targets[int(values[0])] = 0.99
                output = self.forward_pass(inputs)
                change_w = self.backward_pass(targets, output)
                self.update_weights(change_w)

            accuracy = self.compute_accuracy(test_list)
            print(f"Epoch {i+1}/{self.epochs}, Accuracy: {accuracy:.4f}")

            end_time = time.time()
            print(f"Training completed in {end_time - start_time:.2f} seconds")

#increased learning rate for relu
dnn = DNN(sizes=[784, 128, 64, 10], epochs=10, lr=0.005)
dnn.train(train_list, test_list)
