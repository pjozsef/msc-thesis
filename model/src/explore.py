import glob
import sys

import matplotlib.image as mpimg
import numpy as np
from skimage import io

print(sys.executable)


# hello = tf.constant('Hello, TensorFlow!')
# sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
# print(sess.run(hello))


def print_info(arr):
    print(arr.dtype)
    print(type(arr))
    print(arr.shape)
    print(arr)


def print_img(img):
    io.imshow(img)
    io.show()


baseDir = '/Users/jpollak/ppp/thesis-msc/*__*.png'
# io.imshow(img)
# io.show()

# images = io.imread_collection('/Users/jpollak/ppp/thesis-msc/*.png')
# for i in images:
#     print_info(i)

for path in glob.glob(baseDir):
    print(path)

imgs = [mpimg.imread(p) for p in glob.glob(baseDir)]
size = len(imgs)

images = np.empty([size, 800, 20])

for i in range(0, size):
    images[i] = imgs[i]
    # io.imshow(container[i])
    # io.show()

subset = images[:, :200, :]
mean = subset.mean(0)
variance = subset.std(0)

print_info(mean)
print_img(mean)
print_info(variance)
print_img(variance)
