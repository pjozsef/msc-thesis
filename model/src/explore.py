import argparse
import glob

import matplotlib.image as mpimg
import numpy as np
from skimage import io

parser = argparse.ArgumentParser()
parser.add_argument('--data-glob', required=True)
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--export')
args = parser.parse_args()

if args.verbose:
    for path in glob.glob(args.data_glob):
        print(path)

images = [mpimg.imread(p) for p in glob.glob(args.data_glob)]

if args.verbose:
    print("Read images shape:", np.shape(images))

mean = np.mean(images, axis=0)
std = np.std(images, axis=0)
if args.verbose:
    print("Mean:", mean)
    print("Standard deviation", std)

if args.export:
    io.imsave(args.export + "/mean.png", mean)
    io.imsave(args.export + "/std.png", std)
