import glob
import sys

import matplotlib.image as mpimg
import numpy as np
from skimage import io

print(sys.executable)


def print_info(arr):
    print(arr.dtype)
    print(type(arr))
    print(arr.shape)
    print(arr)


def print_img(img):
    io.imshow(img)
    io.show()


baseDir = '/Users/jpollak/Desktop/train_data/*__*.png'

for path in glob.glob(baseDir):
    print(path)

imgs = [mpimg.imread(p) for p in glob.glob(baseDir)]
size = len(imgs)

images = np.empty([size, 800, 20])

for i in range(0, size):
    images[i] = imgs[i]

mean = images.mean(0)
variance = images.std(0)

io.imsave("mean.png", mean)
io.imsave("std.png", variance)
