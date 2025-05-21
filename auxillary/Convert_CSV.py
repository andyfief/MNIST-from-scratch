# This file converts ubyte files to csv files.

import matplotlib.pyplot as plt
import time
import numpy as np

mnist_train_x = './MNIST_Data/train-images.idx3-ubyte'
mnist_train_y = './MNIST_Data/train-labels.idx1-ubyte'
mnist_test_x = './MNIST_Data/t10k-images.idx3-ubyte'
mnist_test_y = './MNIST_Data/t10k-labels.idx1-ubyte'

def convert(imgs, labels, outfile, n):
    imgf = open(imgs, "rb")
    labelf = open(labels, 'rb')
    csvf = open(outfile, 'w')

    imgf.read(16)
    labelf.read(8)
    images = []

    for i in range(n):
        image = [ord(labelf.read(1))]
        for j in range(28*28):
            image.append(ord(imgf.read(1)))
        images.append(image)

    for image in images:
        csvf.write(",".join(str(pix) for pix in image)+"\n")
    imgf.close()
    labelf.close()
    csvf.close()

convert(mnist_train_x, mnist_train_y, './MNIST_Data/train.csv', 60000)
convert(mnist_test_x, mnist_test_y, 'MNIST_Data/test.csv', 10000)

train_file = open('./MNIST_Data/train.csv', 'r')
train_list = train_file.readlines()
train_file.close()

print(len(train_list))

values = train_list[100].split(",")
image_array = np.asarray(values[1:], dtype=float).reshape((28, 28))

plt.figure(figsize=(6, 6))
plt.imshow(image_array, cmap="Greys", interpolation="None")
plt.title(f"MNIST Digit: {values[0]}")
plt.xticks([])
plt.yticks([])
plt.show()