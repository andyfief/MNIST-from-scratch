import numpy as np
import csv

farthestLeft = 14.5
farthestRight = 14.5
farthestTop = 14.5
farthestBottom = 14.5

def findCenter(img):
    global farthestTop, farthestLeft, farthestRight, farthestBottom
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

    if top < farthestTop:
        farthestTop = top
    if left < farthestLeft:
        farthestLeft = left
    if right > farthestRight:
        farthestRight = right
    if bottom > farthestBottom:
        farthestBottom = bottom

    return offset
    
def harden_lines(img):
    for i in range(0, len(img)):
        if(img[i] > 50):
            img[i] = 255
        else:
            img[i] = 0

    return img

def process_all_rows(data, save_file):
    currentRow = 0

    with open(data, 'r') as count_file:
        total_rows = sum(1 for _ in csv.reader(count_file))

    with open(data, 'r') as csvfile:
        with open(save_file, 'w') as outfile:
            read_csv = csv.reader(csvfile)
            print(f"Processing {total_rows} rows...")

            for i, csv_row in enumerate(read_csv):
                if i <= total_rows - 1:
                    values = [int(x) for x in csv_row]
                    label = values[0]
                    pixel_data = values[1:]
                    img = np.array(pixel_data).reshape(28, 28)
                    
                    findCenter(img)
                    img = img.flatten()
                    img = harden_lines(img)
                    img = np.concatenate(([label], img))

                    row_str = ','.join(map(str, img))
                    #outfile.write(row_str + '\n')
                    currentRow += 1

                if currentRow % 100 == 0:
                    print(f"Processed {currentRow}/{total_rows} rows")

    print("Processing complete!")
                        
process_all_rows("MNIST_Data/binary_centered_train.csv", "MNIST_Data/binary_centered_train2.csv")

print(f"Farthest Top: {farthestTop} \n Farthest Bottom: {farthestBottom} \n Farthest Left: {farthestLeft} \n Farthest Right: {farthestRight}")

"""
From cleaned and shifted train:
Farthest Top: 4
 Farthest Bottom: 24
 Farthest Left: 4
 Farthest Right: 24
"""