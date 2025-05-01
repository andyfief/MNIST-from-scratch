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
    <div className="App">
      <header className="App-header">
        <h1>Digit Recognition App</h1>
      </header>
      <main>
        <p>Draw a digit (0-9) in the canvas below:</p>
        <Canvas onSubmit={handleSubmit} />
        
        {isLoading && <p>Processing your drawing...</p>}
        {error && <p className="error">{error}</p>}
        {prediction && <PredictionResult result={prediction} />}
      </main>
    </div>
  );
}

export default App;
