import numpy as np
import csv

    
def soften_lines(img):
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
            print(f"Processing {total_rows} rows...")

            for i, csv_row in enumerate(read_csv):
                if i <= total_rows - 1:
                    values = [int(x) for x in csv_row]
                    label = values[0]
                    pixel_data = values[1:]
                    img = np.array(pixel_data).reshape(28, 28)

                    img = soften_lines(img)
                    
                    img = img.flatten()
                    img = np.concatenate(([label], img))

                    row_str = ','.join(map(str, img))
                    outfile.write(row_str + '\n')
                    currentRow += 1

                if currentRow % 100 == 0:
                    print(f"Processed {currentRow}/{total_rows} rows")

    print("Processing complete!")
                        
process_all_rows("binary_centered_train.csv", "trinary_centered_train.csv")