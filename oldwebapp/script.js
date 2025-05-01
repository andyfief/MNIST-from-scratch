/**
 * MNIST Digit Recognition Web Application
 * 
 * This script handles:
 * 1. Displaying a sample MNIST digit (the number 5)
 * 2. Setting up a canvas for users to draw their own digit
 * 3. Processing the drawn digit for prediction
 * 4. Sending the processed image to a backend API
 * 5. Displaying prediction results
 */

// =============================================================================
// CONSTANTS AND CONFIGURATION
// =============================================================================

// API endpoint for sending digit images for prediction
const API_URL = 'http://localhost:5000/predict';

// Canvas dimensions
const DISPLAY_SIZE = 280;  // Size of drawing canvas in pixels
const MODEL_SIZE = 28;     // Size expected by the MNIST model (28x28 pixels)

// Sample MNIST digit data (number "5") - array of grayscale pixel values (0-255) 
const samplePixelValues = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,255,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,128,128,255,255,255,255,255,255,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,255,255,128,128,128,128,128,255,128,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,128,255,128,128,128,128,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,128,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,255,255,255,255,255,255,128,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,255,255,255,255,255,255,255,255,255,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,255,255,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
];

// =============================================================================
// INITIALIZATION - Runs when DOM is fully loaded
// =============================================================================
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const sampleCanvas = document.getElementById('sample-canvas');
    const canvas = document.getElementById('digit-canvas');
    const predictBtn = document.getElementById('predict-btn');
    const clearBtn = document.getElementById('clear-btn');
    const resultDiv = document.getElementById('result');
    const probBarsDiv = document.getElementById('probability-bars');
    const loadingDiv = document.getElementById('loading');
    
    // Set up drawing context for both canvases
    const sampleCtx = sampleCanvas.getContext('2d');
    const ctx = canvas.getContext('2d');
    
    // Drawing state variables
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    
    // =============================================================================
    // SAMPLE CANVAS SETUP - Displays an example MNIST digit
    // =============================================================================
    
    /**
     * Draws the sample MNIST digit on the sample canvas
     * This gives users an example of what the model expects
     */
    function drawSampleImage() {
        // Constants for sample canvas
        const width = 28;
        const height = 28;
        const scale = 10;  // Scale factor to make the 28x28 image larger
        
        // Clear the canvas
        sampleCtx.clearRect(0, 0, sampleCanvas.width, sampleCanvas.height);
        
        // Draw each pixel from the sample data
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const pixelIndex = y * width + x;
                const pixelValue = samplePixelValues[pixelIndex];
                
                // MNIST values are 0-255, where 0 is background and 255 is foreground
                // Set the color based on the pixel value (grayscale)
                sampleCtx.fillStyle = `rgb(${pixelValue}, ${pixelValue}, ${pixelValue})`;
                
                // Draw a scaled rectangle for each pixel
                sampleCtx.fillRect(x * scale, y * scale, scale, scale);
            }
        }
    }
    
    // =============================================================================
    // MAIN DRAWING CANVAS SETUP - For user input
    // =============================================================================
    
    // Configure the drawing canvas
    ctx.lineWidth = 20;        // Thicker brush for 280x280 display
    ctx.lineJoin = 'round';    // Round line joins for smoother drawing
    ctx.lineCap = 'round';     // Round line caps for smoother drawing
    ctx.strokeStyle = 'white'; // Draw in white on black background
    
    /**
     * Clears the drawing canvas to a black background and resets the UI
     */
    function clearCanvas() {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        resultDiv.textContent = 'Draw a digit and click "Predict"';
        
        // Clear probability bars
        while (probBarsDiv.firstChild) {
            probBarsDiv.removeChild(probBarsDiv.firstChild);
        }
    }
    
    // =============================================================================
    // DRAWING EVENT HANDLERS - Handle mouse and touch input
    // =============================================================================
    
    /**
     * Starts the drawing process when mouse button is pressed
     */
    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }
    
    /**
     * Draws a line as the mouse moves while button is pressed
     */
    function draw(e) {
        if (!isDrawing) return; // Exit if not in drawing mode
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        
        [lastX, lastY] = [e.offsetX, e.offsetY]; // Update position for next draw
    }
    
    /**
     * Stops drawing when mouse button is released
     */
    function stopDrawing() {
        isDrawing = false;
    }
    
    /**
     * Converts touch events to mouse events for drawing on mobile
     */
    function handleTouchStart(e) {
        e.preventDefault(); // Prevent scrolling
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousedown', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }
    
    /**
     * Converts touch move events to mouse events for drawing on mobile
     */
    function handleTouchMove(e) {
        e.preventDefault(); // Prevent scrolling
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }
    
    // =============================================================================
    // PREDICTION HANDLING - Process and send image for prediction
    // =============================================================================
    
    /**
     * Processes the drawn digit and sends it to the API for prediction
     */
    function predictDigit() {
        // Show loading indicator
        loadingDiv.style.display = 'block';
        
        // Create a temporary canvas for downscaling to 28x28 (MNIST format)
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = MODEL_SIZE;
        tempCanvas.height = MODEL_SIZE;
        const tempCtx = tempCanvas.getContext('2d');
        
        // Scale down the drawing to 28x28
        tempCtx.drawImage(canvas, 0, 0, DISPLAY_SIZE, DISPLAY_SIZE, 0, 0, MODEL_SIZE, MODEL_SIZE);
        
        // Get the image data
        const originalImageData = tempCtx.getImageData(0, 0, MODEL_SIZE, MODEL_SIZE);
        
        // Apply softening to the image data to match MNIST characteristics
        const softenedImageData = softenLines(originalImageData, MODEL_SIZE, MODEL_SIZE);
        
        // Put the softened image data back onto the canvas
        tempCtx.putImageData(softenedImageData, 0, 0);
        
        // Display a preview of the processed image
        createAndDisplaySoftenedImagePreview(softenedImageData, MODEL_SIZE, MODEL_SIZE);
        
        // Convert canvas to data URL for sending to API
        const dataUrl = tempCanvas.toDataURL('image/png');
        
        // Send to API
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: dataUrl
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingDiv.style.display = 'none';
            
            // Display result
            resultDiv.textContent = `Predicted Digit: ${data.predicted_digit}`;
            
            // Update probability bars
            updateProbabilityBars(data.probabilities);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingDiv.style.display = 'none';
            resultDiv.textContent = 'Error: Could not get prediction';
        });
    }
    
    /**
     * Creates a visual preview of the processed image that will be sent to the model
     */
    function createAndDisplaySoftenedImagePreview(imageData, width, height) {
        // Create a small display div
        const previewDiv = document.createElement('div');
        previewDiv.style.position = 'fixed';
        previewDiv.style.bottom = '10px';
        previewDiv.style.right = '10px';
        previewDiv.style.padding = '10px';
        previewDiv.style.background = 'white';
        previewDiv.style.border = '1px solid black';
        previewDiv.style.zIndex = '1000';
        
        // Add a title
        const title = document.createElement('h3');
        title.textContent = 'Softened Image Preview';
        title.style.margin = '0 0 5px 0';
        previewDiv.appendChild(title);
        
        // Create a canvas to display the preview (5x larger for visibility)
        const previewCanvas = document.createElement('canvas');
        previewCanvas.width = width * 5;
        previewCanvas.height = height * 5;
        previewCanvas.style.border = '1px solid black';
        
        // Create a temporary canvas at original size
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = width;
        tempCanvas.height = height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.putImageData(imageData, 0, 0);
        
        // Draw the scaled-up version
        const previewCtx = previewCanvas.getContext('2d');
        previewCtx.imageSmoothingEnabled = false; // Disable anti-aliasing for crisp pixels
        previewCtx.drawImage(tempCanvas, 0, 0, width, height, 0, 0, width * 5, height * 5);
        
        previewDiv.appendChild(previewCanvas);
        
        // Add a close button
        const closeButton = document.createElement('button');
        closeButton.textContent = 'Close';
        closeButton.onclick = function() {
            document.body.removeChild(previewDiv);
        };
        previewDiv.appendChild(closeButton);
        
        // Add the preview to the page
        document.body.appendChild(previewDiv);
    }
    
    /**
     * Updates the UI to display prediction probabilities for each digit
     */
    function updateProbabilityBars(probabilities) {
        // Clear existing bars
        while (probBarsDiv.firstChild) {
            probBarsDiv.removeChild(probBarsDiv.firstChild);
        }
        
        // Create new bars - one for each digit (0-9)
        probabilities.forEach((prob, index) => {
            const barContainer = document.createElement('div');
            barContainer.style.display = 'flex';
            barContainer.style.flexDirection = 'column';
            barContainer.style.alignItems = 'center';
            
            // The bar height represents the probability
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = `${prob * 180}px`; // Scale to max height
            
            // Label for the digit
            const label = document.createElement('div');
            label.className = 'bar-label';
            label.textContent = index;
            
            // Label for the probability percentage
            const probLabel = document.createElement('div');
            probLabel.textContent = (prob * 100).toFixed(1) + '%';
            probLabel.style.fontSize = '12px';
            
            // Assemble and add to display
            barContainer.appendChild(bar);
            barContainer.appendChild(label);
            barContainer.appendChild(probLabel);
            
            probBarsDiv.appendChild(barContainer);
        });
    }
    
    // =============================================================================
    // EVENT LISTENERS - Wire up UI elements to their handlers
    // =============================================================================
    
    // Mouse event listeners for drawing
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch event listeners for mobile support
    canvas.addEventListener('touchstart', handleTouchStart);
    canvas.addEventListener('touchmove', handleTouchMove);
    canvas.addEventListener('touchend', stopDrawing);
    
    // Button event listeners
    clearBtn.addEventListener('click', clearCanvas);
    predictBtn.addEventListener('click', predictDigit);
    
    // =============================================================================
    // INITIALIZE APPLICATION
    // =============================================================================
    
    // Draw the sample image
    drawSampleImage();
    
    // Initialize the drawing canvas
    clearCanvas();
});

// =============================================================================
// IMAGE PROCESSING UTILITIES - Outside the DOMContentLoaded event
// =============================================================================

/**
 * Softens the edges of the drawn digit to better match MNIST characteristics
 * This helps improve prediction accuracy by making hand-drawn digits more
 * similar to the training data used in the MNIST model
 */
function softenLines(imageData, width, height) {
    // Create a copy of the image data to work with
    const originalData = imageData.data;
    const softened = new Uint8ClampedArray(originalData.length);
    
    // Copy the original data
    for (let i = 0; i < originalData.length; i++) {
        softened[i] = originalData[i];
    }
    
    /**
     * Gets the pixel value at a specific coordinate
     */
    function getPixel(x, y) {
        if (x < 0 || y < 0 || x >= width || y >= height) {
            return 0; // Out of bounds
        }
        // Each pixel is 4 values (RGBA)
        const index = (y * width + x) * 4;
        // Since we're working with grayscale, just return the red channel
        return originalData[index];
    }
    
    /**
     * Sets the pixel value at a specific coordinate
     */
    function setPixel(x, y, value) {
        if (x < 0 || y < 0 || x >= width || y >= height) {
            return; // Out of bounds
        }
        // Each pixel is 4 values (RGBA)
        const index = (y * width + x) * 4;
        // Set RGB to the same value (grayscale) and keep alpha at 255
        softened[index] = softened[index + 1] = softened[index + 2] = value;
        softened[index + 3] = 255; // Alpha channel
    }
    
    // Apply softening effect by adding gray pixels around white pixels
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const pixelValue = getPixel(x, y);
            
            // Check if this is a white pixel (255)
            if (pixelValue === 255) {
                // Add gray (128) pixels around white pixels when they're adjacent to black (0) pixels
                // This creates a soft edge effect
                if (x + 1 < width && getPixel(x + 1, y) === 0) {
                    setPixel(x + 1, y, 128);
                }
                if (x - 1 >= 0 && getPixel(x - 1, y) === 0) {
                    setPixel(x - 1, y, 128);
                }
                if (y + 1 < height && getPixel(x, y + 1) === 0) {
                    setPixel(x, y + 1, 128);
                }
                if (y - 1 >= 0 && getPixel(x, y - 1) === 0) {
                    setPixel(x, y - 1, 128);
                }
            }
        }
    }
    
    // Create and return a new ImageData object with the softened pixels
    return new ImageData(softened, width, height);
}