#This file cleans raw MNIST image data in both test.csv and train.csv
#Modify input and output files at the bottom of this script.

import numpy as np
import csv

    
def findCenter(img):
    
    #image dimensions
    height, width = img.shape

    # Top of number (scan top-down)
    top = 0
    while top < height:
        if any(img[top, i] > 0 for i in range(width)):
            break
        top += 1

    # Bottom of number (scan bottom-up)
    bottom = height - 1
    while bottom >= 0:
        if any(img[bottom, i] > 0 for i in range(width)):
            break
        bottom -= 1

    # Left of number (scan left-right)
    left = 0
    while left < width:
        if any(img[i, left] > 0 for i in range(height)):
            break
        left += 1

    # Right of number (scan right-left)
    right = width - 1
    while right >= 0:
        if any(img[i, right] > 0 for i in range(height)):
            break
        right -= 1

    #height of the drawn number
    numberHeight = bottom - top + 1
    numberWidth = right - left + 1

    target_y = (height - numberHeight) // 2
    target_x = (width - numberWidth) // 2

    y_offset = target_y - top
    x_offset = (target_x) - left

    offset = [y_offset, x_offset]

    return offset

def shiftImage(img, offset):
    height, width = img.shape
    
    shifted_img = np.zeros((height, width), dtype=img.dtype)
    
    y_offset = offset[0]
    x_offset = offset[1]
    
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
    
    shifted_img[dst_y_range, dst_x_range] = img[src_y_range, src_x_range]

    return shifted_img
    
def harden_lines(img):
    for i in range(0, len(img)):
        if(img[i] > 50):
            img[i] = 255
        else:
            img[i] = 0

    return img

def soften_edges(img):
    for i in range(0, 28):
        for j in range(0, 28):
            if(img[i, j] == 255 and img[i + 1, j] == 0):
                img[i + 1, j] = 128
            if(img[i, j] == 255 and img[i - 1, j] == 0):
                img[i - 1, j] = 128
            if(img[i, j] == 255 and img[i, j + 1] == 0):
                img[i, j + 1] = 128
            if(img[i, j] == 255 and img[i, j - 1] == 0):
                img[i, j - 1] = 128
    return img

def process_all_rows(data, save_file):
    currentRow = 0

    with open(data, 'r') as count_file:
        total_rows = sum(1 for _ in csv.reader(count_file))

    with open(data, 'r') as csvfile:
        with open(save_file, 'w') as outfile:
            read_csv = csv.reader(csvfile)
            print(f"Processing {total_rows} rows for {data}...")

            for i, csv_row in enumerate(read_csv):
                if i <= total_rows - 1:
                    values = [int(x) for x in csv_row]
                    label = values[0]
                    pixel_data = values[1:]

                    img = harden_lines(pixel_data)
                    
                    img = np.array(pixel_data).reshape(28, 28)

                    offset = findCenter(img)
                    img = shiftImage(img, offset)

                    img = soften_edges(img)

                    img = img.flatten()
                    img = np.concatenate(([label], img))

                    row_str = ','.join(map(str, img))
                    outfile.write(row_str + '\n')
                    currentRow += 1

                if currentRow % 100 == 0:
                    print(f"Processed {currentRow}/{total_rows} rows")

    print("Processing complete!")
                        
process_all_rows("../MNIST_Data/test.csv", "../MNIST_Data/cleanTest.csv")
process_all_rows("../MNIST_Data/train.csv", "../MNIST_Data/cleanTrain.csv")