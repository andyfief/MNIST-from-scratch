# To use, python mnist_viewer.py --line TargetImageLine --file TargetFile.csv --output OutPutFile.html
# Then open the output file in a browser.
# This works for any image data of length label + 784

import csv
import os
import sys
import argparse

def create_html_for_image(pixel_data, label, index, output_file='mnist_image.html'):
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MNIST Image Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-color: #f0f0f0;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}
        canvas {{
            border: 1px solid #333;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: black;
        }}
        h1 {{
            color: #333;
        }}
        .info {{
            font-size: 14px;
            color: #666;
            max-width: 600px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .controls {{
            margin-bottom: 20px;
        }}
        input, button {{
            padding: 8px;
            margin: 5px;
        }}
        .options {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .options label {{
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>MNIST Image Viewer</h1>
        <div class="info">
            Displaying image #{index} from test.csv<br>
            Label: {label} (digit "{label}")
        </div>
        <div class="controls">
            <form action="" method="get">
                <label for="image_index">Image Index:</label>
                <input type="number" id="image_index" name="n" min="0" value="{index}">
                <button type="submit">Load Image</button>
            </form>
        </div>
        <div class="options">
            <label for="show_grid">Show Grid:</label>
            <input type="checkbox" id="show_grid" checked>
            
            <label for="grid_color" style="margin-left: 15px;">Grid Color:</label>
            <select id="grid_color">
                <option value="rgba(100, 100, 100, 0.5)">Gray</option>
                <option value="rgba(0, 100, 200, 0.5)">Blue</option>
                <option value="rgba(200, 50, 50, 0.5)">Red</option>
                <option value="rgba(0, 150, 0, 0.5)">Green</option>
            </select>
        </div>
        <canvas id="imageCanvas" width="280" height="280"></canvas>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const canvas = document.getElementById('imageCanvas');
            const ctx = canvas.getContext('2d');
            const showGridCheckbox = document.getElementById('show_grid');
            const gridColorSelect = document.getElementById('grid_color');
            
            const pixelValues = [{pixel_data_str}];
            
            const width = 28;
            const height = 28;
            const scale = 10;
            
            function drawImage() {{
                // Clear the canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // First draw the pixel data
                for (let y = 0; y < height; y++) {{
                    for (let x = 0; x < width; x++) {{
                        const pixelIndex = y * width + x;
                        const pixelValue = parseInt(pixelValues[pixelIndex]);
                        
                        const color = pixelValue;
                        ctx.fillStyle = `rgb(${{color}}, ${{color}}, ${{color}})`;
                        
                        ctx.fillRect(x * scale, y * scale, scale, scale);
                    }}
                }}
                
                // Draw the grid if checkbox is checked
                if (showGridCheckbox.checked) {{
                    drawGrid();
                }}
            }}
            
            function drawGrid() {{
                const gridColor = gridColorSelect.value;
                ctx.strokeStyle = gridColor;
                ctx.lineWidth = 0.5;
                
                // Draw vertical lines
                for (let x = 0; x <= width; x++) {{
                    ctx.beginPath();
                    ctx.moveTo(x * scale, 0);
                    ctx.lineTo(x * scale, height * scale);
                    ctx.stroke();
                }}
                
                // Draw horizontal lines
                for (let y = 0; y <= height; y++) {{
                    ctx.beginPath();
                    ctx.moveTo(0, y * scale);
                    ctx.lineTo(width * scale, y * scale);
                    ctx.stroke();
                }}
            }}
            
            // Initial draw
            drawImage();
            
            // Add event listeners for UI controls
            showGridCheckbox.addEventListener('change', drawImage);
            gridColorSelect.addEventListener('change', drawImage);
        }});
    </script>
</body>
</html>
    """
    
    pixel_data_str = ",".join(str(p) for p in pixel_data)
    
    html_content = html_template.format(
        pixel_data_str=pixel_data_str,
        label=label,
        index=index
    )
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"HTML file created: {output_file}")
    print(f"Open this file in a web browser to view the image.")

def read_mnist_csv(file_path, line_index):
    try:
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            
            current_line = 0
            for row in csv_reader:
                if current_line == line_index:
                    label = row[0]
                    pixel_values = row[1:] if len(row) > 1 else []
                    return label, pixel_values
                current_line += 1
                
        raise ValueError(f"Line {line_index} not found in {file_path}")
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Display an MNIST image from a CSV file')
    parser.add_argument('--file', default='test.csv', help='Path to the CSV file (default: test.csv)')
    parser.add_argument('--line', type=int, default=0, help='Line number to read (0-based, default: 0)')
    parser.add_argument('--output', default='mnist_image.html', help='Output HTML file (default: mnist_image.html)')
    args = parser.parse_args()
    
    label, pixel_values = read_mnist_csv(args.file, args.line)
    create_html_for_image(pixel_values, label, args.line, args.output)

if __name__ == "__main__":
    main()