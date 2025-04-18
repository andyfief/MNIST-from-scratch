import numpy as np
import csv

    
def getArr(file_path, row_index):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, csv_row in enumerate(csv_reader):
            if i == row_index:
                values = [int(x) for x in csv_row]
                
                label = values[0]
                pixel_data = values[1:]
                image = np.array(pixel_data).reshape(28, 28)
                return label, image
    # If row_index is out of bounds
    raise IndexError("Row index out of range")


def findCenter(img):

    #image dimensions
    height, width = img.shape

    # Top of drawn number (scan top-down)
    top = 0
    while top < height:
        if any(img[top, i] > 0 for i in range(width)):
            break
        top += 1

    # Bottom of drawn number (scan bottom-up)
    bottom = height - 1
    while bottom >= 0:
        if any(img[bottom, i] > 0 for i in range(width)):
            break
        bottom -= 1

    # Left of drawn number (scan left-right)
    left = 0
    while left < width:
        if any(img[i, left] > 0 for i in range(height)):
            break
        left += 1

    # Right of drawn number (scan right-left)
    right = width - 1
    while right >= 0:
        if any(img[i, right] > 0 for i in range(height)):
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

def shiftImage(img, offset):
    height, width = img.shape
    
    # Create a new blank image
    shifted_img = np.zeros((height, width), dtype=img.dtype)
    
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
    shifted_img[dst_y_range, dst_x_range] = img[src_y_range, src_x_range]
    
    return shifted_img

def harden_lines(img):
    for i in range(0, len(img)):
        if(img[i] > 50):
            img[i] = 255
        else:
            img[i] = 0

    return img

def save_to_csv(label_and_img, file_path, mode='a'):
    """
    Save a 1D array containing a label and image data to a CSV file.
    
    Args:
        label_and_img: 1D numpy array with label as first element and flattened image as rest
        file_path: Path to the CSV file
        mode: 'a' for append (default), 'w' for write (overwrites existing file)
    """
    # Convert numpy array to a comma-separated string
    row_str = ','.join(map(str, label_and_img))
    
    # Write to file
    with open(file_path, mode) as f:
        if mode == 'w':
            # If writing a new file, you might want to add a header
            # f.write("label,pixel0,pixel1,...,pixel783\n")
            pass
        f.write(row_str + '\n')


def process_all_rows(input_csv, output_csv):
    # Initialize row counter
    row_count = 0
    output_mode = 'w'  # Start with write mode to create/overwrite file
    
    # Try to determine total number of rows for progress reporting
    with open(input_csv, 'r') as csvfile:
        total_rows = sum(1 for _ in csv.reader(csvfile))
    
    print(f"Processing {total_rows} rows...")
    
    # Process each row
    while True:
        try:
            # Get the image and label for the current row
            label, img = getArr(input_csv, row_count)
            
            # Find the center and shift the image
            offset = findCenter(img)
            shifted_img = shiftImage(img, offset)
            
            # Process the image data
            flattened_img = shifted_img.flatten()
            hardened_img = harden_lines(flattened_img)
            label_and_img = np.concatenate(([label], hardened_img))
            
            # Save to CSV
            save_to_csv(label_and_img, output_csv, mode=output_mode)
            
            # After first write, switch to append mode
            if output_mode == 'w':
                output_mode = 'a'
            
            # Increment row counter
            row_count += 1
            
            # Print progress periodically
            if row_count % 100 == 0:
                print(f"Processed {row_count}/{total_rows} rows")
                
        except IndexError:
            # We've reached the end of the file
            print(f"Completed processing {row_count} rows")
            break
        except Exception as e:
            # Handle any other errors
            print(f"Error processing row {row_count}: {e}")
            row_count += 1  # Skip this row and continue
    
    print("Processing complete!")

process_all_rows("train.csv", "binary_centered_train.csv")


"""

Have 4 lines, two vertical two horizonal
start at 0,0 28,28

move each line in until a member of that line is nonzero
continue until all 4 lines have stopped
intersections of lines are bounding box




"""