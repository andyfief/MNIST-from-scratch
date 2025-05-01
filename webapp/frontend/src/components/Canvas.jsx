import React, {useState, useRef} from 'react';

function Canvas( {onSubmit }){
  const canvasRef = useRef(null);
  const[isDrawing, setIsDrawing] = useState(false);

  const width = 28;
  const height = 28;

  React.useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
  }, []);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.beginPath();

    const scaleX = width / (width * 10);
    const scaleY = height / (height * 10);
    const x = e.nativeEvent.offsetX * scaleX;
    const y = e.nativeEvent.offsetY * scaleY;
    ctx.moveTo(x, y);

    setIsDrawing(true);
  };

  const draw = (e) => {
    if(!isDrawing) {
      return;
    }
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    const scaleX = width / (width * 10);
    const scaleY = height / (height * 10);
    const x = e.nativeEvent.offsetX * scaleX;
    const y = e.nativeEvent.offsetY * scaleY;
    ctx.lineTo(x, y);

    ctx.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  }

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
  };

  const getImageData = () => {
    const canvas = canvasRef.current;
    const dataURL = canvas.toDataURL('image/png');
    // Remove the "data:image/png;base64," part
    const base64Image = dataURL.split(',')[1];
    onSubmit(base64Image);
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{ border: '1px solid black', width: `${width * 10}px`, height: `${height * 10}px`, imageRendering: 'pixelated' }}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
      />
      <div style={{ marginTop: '10px' }}>
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={getImageData}>Predict</button>
      </div>
    </div>
  );
}

export default Canvas;