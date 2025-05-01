import matplotlib.pyplot as plt
import time
import numpy as np
import pickle

train_file = open('./MNIST_Data/trinary_centered_train.csv', 'r')
train_list = train_file.readlines()
train_file.close()

test_file = open('./MNIST_Data/trinary_centered_test.csv', 'r')
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
            'W1':np.random.randn(hidden_1, input_layer) * np.sqrt(1./hidden_1), # 128 x 784
            'W2':np.random.randn(hidden_2, hidden_1) * np.sqrt(1./hidden_2), # 64 x 128
            'W3':np.random.randn(output_layer, hidden_2) * np.sqrt(1./output_layer) # 10 x 64
        }

    # sets values to be between 0 and 1
    def sigmoid(self, x, derivative=False):
        if derivative:
            return (np.exp(-x))/((np.exp(-x)+1)**2)
        return 1/(1+np.exp(-x))
    
    # For the output layer
    # Converts scores to probabilities, and all outputs sum to 1
    def softmax(self, x, derivative=False):
        exps = np.exp(x-x.max())
        if derivative:
            return exps / np.sum(exps, axis = 0) * (1-exps / np.sum(exps, axis = 0))
        return exps / np.sum(exps, axis = 0)

    def forward_pass(self, x_train):
        params = self.params

        # take inputs from previous layer
        # compute weighted sum Z = W*A using dot product
        # apply activation function to get output A = activation(Z)

        params['A0'] = x_train # 784 x 1

        # input layer to hidden_1
        params['Z1'] = np.dot(params['W1'], params['A0']) # 128 x 1
        params['A1'] = self.sigmoid(params['Z1'])

        # hidden1 to hidden2
        params['Z2'] = np.dot(params['W2'], params['A1'])
        params['A2'] = self.sigmoid(params['Z2'])

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
        error = np.dot(params['W3'].T, error) * self.sigmoid(params['Z2'], derivative=True)
        change_w['W2'] = np.outer(error, params['A1'])

        # calculate W1 update
        error = np.dot(params['W2'].T, error) * self.sigmoid(params['Z1'], derivative=True)
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


def save_model_weights(model, filename='trinary_mnist_model_weights.pkl'):
    weights = {
        'W1': model.params['W1'],
        'W2': model.params['W2'],
        'W3': model.params['W3']
    }

    with open(filename, 'wb') as f:
        pickle.dump(weights, f)
    
    print(f"Model weights saved to {filename}")
    

dnn = DNN(sizes=[784, 128, 64, 10], epochs=10, lr=0.001)
dnn.train(train_list, test_list)
save_model_weights(dnn)

"""
Epoch 1/10, Accuracy: 0.8449
Epoch 2/10, Accuracy: 0.8732
Epoch 3/10, Accuracy: 0.8824
Epoch 4/10, Accuracy: 0.8895
Epoch 5/10, Accuracy: 0.8965
Epoch 6/10, Accuracy: 0.9029
Epoch 7/10, Accuracy: 0.9079
Epoch 8/10, Accuracy: 0.9101
Epoch 9/10, Accuracy: 0.9107
Epoch 10/10, Accuracy: 0.9123
"""