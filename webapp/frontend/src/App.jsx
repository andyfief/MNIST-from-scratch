import React, {useState} from 'react';
import Canvas from './components/Canvas';
import PredictionResult from './components/PredictionResult';
import ScrollDownPtr from './components/ScrollDownPtr';
import{ predictDigit } from './services/api';
import './styles/App.css';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (imageData) => {
    setIsLoading(true);
    setError(null);

    try{
      const result = await predictDigit(imageData);
      setPrediction(result);
    } catch (error) {
      setError('Error predicting digit. Please try again');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="App">
        <div className="canvas-screen">
          <Canvas onSubmit={handleSubmit} />
        </div>
        <div className="prediction-screen">
          {prediction && <PredictionResult result={prediction} />}
        </div>
        
        <div className="background-image">
        <div className="scrollDown">
            <ScrollDownPtr />
          </div>
        </div>
        
        {error && <p className="error">{error}</p>}
    </div>
      <div className="information-section">
          <p id = 'tutorialLine'>Draw a digit in the left screen and click "Predict" to see the neural network classify your handwriting!</p>
          <h3 id='tips'>Tips</h3>
          <p className = 'tipsLines'> Fill up most of the square.</p>
          <p className = 'tipsLines'> Use a straight 1, without a base.</p>
          <p className = 'tipsLines'> Use an empty 0, without the slash.</p>
          <h3>About the MNIST Dataset</h3>
          <p>The MNIST database is a large collection of handwritten digits used for training various image processing systems.</p>
          <p>It contains 70,000 images of handwritten digits (0-9) and each image is a 28×28 grayscale pixel grid. </p>
          <p>This page is an interface for a neural network written from scratch- no frameworks like PyTorch or TensorFlow were used.</p>
          <h3>About the Nueral Network</h3>
          <p>The Neural Network is written entirely from scratch in Python and Numpy, down to the matrix multiplications and derivatives.
              </p>
          
          
      </div>
    </div>
  );
}

export default App;
