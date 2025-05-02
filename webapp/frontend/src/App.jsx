import React, {useState} from 'react';
import Canvas from './components/Canvas';
import PredictionResult from './components/PredictionResult';
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

        <div className="background-image"></div>
        
        {error && <p className="error">{error}</p>}
    </div>
      <div className="information-section">
          <h3>About the MNIST Dataset</h3>
          <p>The MNIST database (Modified National Institute of Standards and Technology) is a large collection of handwritten digits widely used for training various image processing systems.</p>
          <p>It contains 70,000 images of handwritten digits (0-9), with 60,000 for training and 10,000 for testing. Each image is a 28×28 grayscale pixel grid.</p>
          <p>Draw a digit in the left screen and click "Predict" to see our neural network classify your handwriting!</p>
      </div>
    </div>
  );
}

export default App;
