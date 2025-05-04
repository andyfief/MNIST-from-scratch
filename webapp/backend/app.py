import numpy as np
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS  # Enables Cross-Origin Resource Sharing for the API
import base64  # For encoding/decoding base64 image data
import io  # For handling byte streams
from PIL import Image  # Python Imaging Library for image processing


import pickle  # Serialization/deserialization for loading the model weights

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
model.load_weights('./models/trinary_mnist_model_weights.pkl')  # Update with your actual weights file path

def processRequest(image_data):
    # Remove the data URL prefix if present
        if image_data.startswith('data:image/'):
            image_data = image_data.split(',')[1]
        # Decode the base64 image
        decoded = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded)).convert('L')  # Convert to grayscale
        # Resize to 28x28 (MNIST standard size)
        image = image.resize((28, 28))
        # Convert to numpy array and normalize
        image_array = np.array(image).astype('float32')
        # flips it to white on black and normalizes values
        image_array = np.where(image_array < 100, 255, 0)

        return image_array

def findCenter(image):
            #image dimensions
            height, width = image.shape

            # Top of drawn number (scan top-down)
            top = 0
            while top < height:
                if any(image[top, i] > 0 for i in range(width)):
                    break
                top += 1

            # Bottom of drawn number (scan bottom-up)
            bottom = height - 1
            while bottom >= 0:
                if any(image[bottom, i] > 0 for i in range(width)):
                    break
                bottom -= 1

            # Left of drawn number (scan left-right)
            left = 0
            while left < width:
                if any(image[i, left] > 0 for i in range(height)):
                    break
                left += 1

            # Right of drawn number (scan right-left)
            right = width - 1
            while right >= 0:
                if any(image[i, right] > 0 for i in range(height)):
                    break
                right -= 1

            #height of the drawn number
            numberHeight = bottom - top
            numberWidth = right - left

            # center of the drawn number
            Y = top + (numberHeight / 2)
            X = left + (numberWidth / 2)

            imageCenter = [height / 2, width / 2]
            numberCenter = [X, Y]

            offset = [imageCenter[0] - numberCenter[0], imageCenter[1] - numberCenter[1]]

            return offset

def shiftImage(image, offset):
            height, width = image.shape
            
            # Create a new blank image
            shifted_image = np.zeros((height, width), dtype=image.dtype)
            
            # Round offset values to nearest whole pixel (or 0.5 if needed)
            x_offset = round(offset[0])
            y_offset = round(offset[1])
            
            if x_offset >= 0:
                src_x_range = slice(0, width - x_offset)
                dst_x_range = slice(x_offset, width)
            else:
                src_x_range = slice(-x_offset, width)
                dst_x_range = slice(0, width + x_offset)
                
            if y_offset >= 0:
                src_y_range = slice(0, height - y_offset)
                dst_y_range = slice(y_offset, height)
            else:
                src_y_range = slice(-y_offset, height)
                dst_y_range = slice(0, height + y_offset)
            
            # Copy the relevant part of the image
            shifted_image[dst_y_range, dst_x_range] = image[src_y_range, src_x_range]

            return shifted_image

def softenEdges(image):
      # get the trinary black-grey-white image format that we trained the model on. Grey values are edges.
        for i in range(28):
            for j in range(28):
                if image[i, j] == 255:
                    if i + 1 < 28 and image[i + 1, j] == 0:
                        image[i + 1, j] = 128
                    if i - 1 >= 0 and image[i - 1, j] == 0:
                        image[i - 1, j] = 128
                    if j + 1 < 28 and image[i, j + 1] == 0:
                        image[i, j + 1] = 128
                    if j - 1 >= 0 and image[i, j - 1] == 0:
                        image[i, j - 1] = 128
        return image

def viewInFile(image_array):
    #image_array = image_array.flatten() if needed
    import csv
    with open('view.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(image_array)
     
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image data from the request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400
        
        image_array = processRequest(image_data)

        #find the offset of the image's center from the center of the grid
        offset = findCenter(image_array)
        
        #shift drawn image to the center of the grid
        image_array = shiftImage(image_array, offset)

        #add grey on the outside of the white image to indicate edges
        image_array = softenEdges(image_array)
    
        # Flatten the image to 784x1 vector
        image_array = image_array.flatten()
        
        # Make prediction using model
        prediction = model.forward_pass(image_array)
        predicted_class = np.argmax(prediction)
        prediction_probabilities = prediction
        
        return jsonify({
            'predicted_digit': int(predicted_class),
            'probabilities': prediction_probabilities.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)