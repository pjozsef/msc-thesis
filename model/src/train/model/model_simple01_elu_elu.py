from src.train.model_utils import *


def create_model():
    elu = tf.nn.elu
    x = tf.placeholder(tf.float32, [None, 800, 20, 1], name='x')

    conv1 = conv2d(x, [3, 3, 1, 16], "conv1", elu, "VALID")
    conv2 = conv2d(conv1, [3, 3, 16, 16], "conv2", elu, "VALID")
    pool1 = maxpool(conv2)
    conv3 = conv2d(pool1, [5, 5, 16, 32], "conv3", elu, "VALID")
    conv4 = conv2d(conv3, [5, 5, 32, 32], "conv4", elu, "VALID")
    pool2 = maxpool(conv4, 2)
    conv5 = conv2d(pool2, [4, 4, 32, 32], "conv5", elu, "VALID")
    pool3 = maxpool(conv5)
    flattened = flatten(pool3)
    fc1 = fc(flattened, [3072, 512], elu, "fc1")
    fc2 = fc(fc1, [512, 256], elu, "fc2")
    fc3 = fc(fc2, [256, 128], elu, "fc3")
    fc4 = fc(fc3, [128, 64], elu, "fc4")
    encoded = fc(fc4, [64, 32], elu, "fc5", "encoded")
    d_fc5 = decode_fc(encoded, elu, "fc5")
    d_fc4 = decode_fc(d_fc5, elu, "fc4")
    d_fc3 = decode_fc(d_fc4, elu, "fc3")
    d_fc2 = decode_fc(d_fc3, elu, "fc2")
    d_fc1 = decode_fc(d_fc2, elu, "fc1")
    reshaped = tf.reshape(d_fc1, [-1, 96, 1, 32])
    d_pool3 = upsample(reshaped)
    d_conv5 = deconv2d(d_pool3, "conv5", [tf.shape(x)[0], 195, 4, 32], elu, "VALID")
    d_pool2 = upsample(d_conv5, 2)
    d_conv4 = deconv2d(d_pool2, "conv4", [tf.shape(x)[0], 394, 12, 32], elu, "VALID")
    d_conv3 = deconv2d(d_conv4, "conv3", [tf.shape(x)[0], 398, 16, 16], elu, "VALID")
    d_pool1 = upsample(d_conv3)
    d_conv2 = deconv2d(d_pool1, "conv2", [tf.shape(x)[0], 798, 18, 16], elu, "VALID")
    y = deconv2d(d_conv2, "conv1", [tf.shape(x)[0], 800, 20, 1], elu, "VALID")

    return x, encoded, y
