import argparse
import csv
import glob

import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf


def extract_info(path, info_labels, encoded, encoded_dimensions):
    file_name = path.split("/")[-1][:-4]
    parts = file_name.split("__")
    result = {}
    for info, label in zip(parts, info_labels):
        result[label] = info
    for encoding, label in zip(encoded, encoded_dimensions):
        result[label] = encoding
    return result


parser = argparse.ArgumentParser()
parser.add_argument('--data-glob', required=True)
parser.add_argument('--model', required=True)
parser.add_argument('--export', required=True)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    for path in glob.glob(args.data_glob):
        print(path)

glob_input = glob.glob(args.data_glob)
paths = [p for p in glob_input]
images = [mpimg.imread(p) for p in glob_input]

info_labels = ['style', 'artist', 'album', 'song', 'percentile']
encoded_dimensions = [str(i) for i in range(32)]
fieldnames = info_labels + encoded_dimensions

with tf.Session(graph=tf.Graph()) as sess:
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], args.model)
    encoded = sess.graph.get_tensor_by_name("fc5/encoded:0")

    with open(args.export, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        progress = 0
        max = len(paths)
        for path, image in zip(paths, images):
            if progress % 500 == 0:
                print("{:.2f}%".format(progress / float(max) * 100))
            image = np.array(image).reshape([-1, 800, 20, 1])
            codes = np.reshape(
                sess.run(encoded, feed_dict={'x:0': image, 'fc_keep_prob:0': 1.0, 'conv_keep_prob:0': 1.0}), [32])
            writer.writerow(extract_info(path, info_labels, codes, encoded_dimensions))
            if args.verbose:
                print("Finished", path)
                print("Encoding", codes)
            progress += 1
