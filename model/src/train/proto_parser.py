import tensorflow as tf


def parse_proto(proto):
    features = {'height': tf.FixedLenFeature([], tf.int64),
                'width': tf.FixedLenFeature([], tf.int64),
                'name': tf.FixedLenFeature([], tf.string),
                'image_raw': tf.FixedLenFeature([], tf.string)}
    parsed_features = tf.parse_single_example(proto, features)

    height = tf.cast(parsed_features['height'], tf.int32)
    width = tf.cast(parsed_features['width'], tf.int32)
    dim = tf.stack([height, width, 1])
    image = tf.decode_raw(parsed_features['image_raw'], tf.float32)
    image = tf.reshape(image, dim)

    name = tf.cast(parsed_features['name'], tf.string)
    return image, dim, name
