import argparse
import glob

import matplotlib.image as mpimg
import pandas as pd
import tensorflow as tf


def int_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def to_images(paths):
    return [mpimg.imread(f) for f in paths]


def to_examples(path_x_img):
    examples = []
    for path, img in path_x_img:
        height, width = img.shape
        name = path.split('/')[-1]
        feature = {
            'height': int_feature(height),
            'width': int_feature(width),
            'name': bytes_feature(tf.compat.as_bytes(name)),
            'image_raw': bytes_feature(tf.compat.as_bytes(img.tostring()))
        }
        examples.append(tf.train.Example(features=tf.train.Features(feature=feature)))
    return examples


def parse_proto(proto):
    features = {'height': tf.FixedLenFeature([], tf.int64),
                'width': tf.FixedLenFeature([], tf.int64),
                'name': tf.FixedLenFeature([], tf.string),
                'image_raw': tf.FixedLenFeature([], tf.string)}
    parsed_features = tf.parse_single_example(proto, features)

    height = tf.cast(parsed_features['height'], tf.int32)
    width = tf.cast(parsed_features['width'], tf.int32)
    dim = tf.stack([height, width])
    image = tf.decode_raw(parsed_features['image_raw'], tf.float32)
    image = tf.reshape(image, dim)

    name = tf.cast(parsed_features['name'], tf.string)
    return image, dim, name


def print_summary(paths):
    artists = [p.split("/")[-1].split("__")[1] for p in paths]
    frame = pd.DataFrame({"artist": artists})
    pd.set_option('display.max_rows', 10000)
    print("Summary")
    print(frame.describe())
    print()
    print(frame.groupby('artist')['artist'].count())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--result', required=True)
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()

    paths = glob.glob(args.source)

    images = to_images(paths)

    paths_x_images = list(zip(paths, images))

    examples = to_examples(paths_x_images)

    with tf.python_io.TFRecordWriter(args.result) as writer:
        for example in examples:
            writer.write(example.SerializeToString())

    print_summary(paths)

    if args.validate:
        print("Validating tfrecord with original input")
        init_op = tf.group(tf.global_variables_initializer(),
                           tf.local_variables_initializer())
        with tf.Session() as sess:
            sess.run(init_op)
            filenames = tf.placeholder(tf.string, shape=[None])
            dataset = tf.data.TFRecordDataset(filenames)
            dataset = dataset.map(parse_proto)
            dataset = dataset.repeat(1)
            iterator = dataset.make_initializable_iterator()
            sess.run(iterator.initializer, feed_dict={filenames: [args.result]})
            next_element = iterator.get_next()

            for original_path, original_image in paths_x_images:
                parsed_image, parsed_dimension, parsed_name = sess.run(next_element)
                original_name = original_path.split("/")[-1]
                assert parsed_dimension[0] == original_image.shape[0]
                assert parsed_dimension[1] == original_image.shape[1]
                assert parsed_name.decode() == original_name
                assert (parsed_image == original_image).all()
        print("Validation passed")
