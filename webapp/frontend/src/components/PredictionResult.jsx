import React from 'react';

const PredictionResult = ({ result }) => {
    const {predicted_digit, probabilities} = result;

    return (
        <div className="prediction-result">
            <h2>Prediction: {predicted_digit}</h2>
            <h3>Confidence Levels:</h3>
            <div className="probabilities">
            {probabilities.map((prob, index) => (
                <div key={index} className="probability-bar">
                <div className="digit-label">{index}</div>
                <div className="bar-container">
                    <div 
                    className="bar" 
                    style={{ 
                        width: `${Math.round(prob * 100)}%`,
                        backgroundColor: index === predicted_digit ? '#4CAF50' : '#ddd'
                    }}
                    />
                </div>
                <div className="percentage">{(prob * 100).toFixed(2)}%</div>
                </div>
            ))}
            </div>
        </div>
    );
};

export default PredictionResult;