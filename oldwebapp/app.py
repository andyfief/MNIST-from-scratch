from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import base64
import io
from PIL import Image
import sys
import os
import pickle

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DNN:
    def __init__(self, sizes=[784, 128, 64, 10]):
        self.sizes = sizes
        
        input_layer = sizes[0]
        hidden_1 = sizes[1]
        hidden_2 = sizes[2]
        output_layer = sizes[3]
        
        # Initialize params dictionary
        self.params = {
            'W1': None,
            'W2': None,
            'W3': None
        }
        
    def load_weights(self, weights_file):
        # Load weights from pickle file
        with open(weights_file, 'rb') as f:
            weights = pickle.load(f)
        
        # Set the weights
        self.params['W1'] = weights['W1']
        self.params['W2'] = weights['W2']
        self.params['W3'] = weights['W3']
        
        print("Weights loaded successfully")
    
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
        params['A0'] = x_train

        # input layer to hidden_1
        params['Z1'] = np.dot(params['W1'], params['A0'])
        params['A1'] = self.sigmoid(params['Z1'])

        # hidden1 to hidden2
        params['Z2'] = np.dot(params['W2'], params['A1'])
        params['A2'] = self.sigmoid(params['Z2'])

        # hidden2 to output
        params['Z3'] = np.dot(params['W3'], params['A2'])
        params['A3'] = self.softmax(params['Z3'])

        return params['A3']

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize your model
model = DNN(sizes=[784, 128, 64, 10])
model.load_weights('../models/trinary_mnist_model_weights.pkl')  # Update with your actual weights file path

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image data from the request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400
        
        # Remove the data URL prefix if present
        if image_data.startswith('data:image/'):
            image_data = image_data.split(',')[1]
        
        # Decode the base64 image
        decoded = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded)).convert('L')  # Convert to grayscale
        
        # Resize to 28x28 (MNIST standard size)
        image = image.resize((28, 28))
        
        # Convert to numpy array and normalize
        image_array = np.array(image).astype('float32') / 255.0
        
        # Flatten the image to 784x1 vector (as expected by your model)
        image_array = image_array.flatten()
        
        # Make prediction using your model
        prediction = model.forward_pass(image_array)
        predicted_class = np.argmax(prediction)
        
        return jsonify({
            'predicted_digit': int(predicted_class),
            'probabilities': prediction.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)