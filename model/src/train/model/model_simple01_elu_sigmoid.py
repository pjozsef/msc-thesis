from src.train.model_utils import *


def create_model():
    x = tf.placeholder(tf.float32, [None, 800, 20, 1], name='x')

    conv1 = conv2d_elu(x, [3, 3, 1, 16], "conv1", "VALID")
    conv2 = conv2d_elu(conv1, [3, 3, 16, 16], "conv2", "VALID")
    pool1 = maxpool(conv2)
    conv3 = conv2d_elu(pool1, [5, 5, 16, 32], "conv3", "VALID")
    conv4 = conv2d_elu(conv3, [5, 5, 32, 32], "conv4", "VALID")
    pool2 = maxpool(conv4, 2)
    conv5 = conv2d_elu(pool2, [4, 4, 32, 32], "conv5", "VALID")
    pool3 = maxpool(conv5)
    flattened = flatten(pool3)
    fc1 = fc_sigmoid(flattened, [3072, 512], "fc1")
    fc2 = fc_sigmoid(fc1, [512, 256], "fc2")
    fc3 = fc_sigmoid(fc2, [256, 128], "fc3")
    fc4 = fc_sigmoid(fc3, [128, 64], "fc4")
    encoded = fc_sigmoid(fc4, [64, 32], "fc5", "encoded")
    d_fc5 = decode_fc_sigmoid(encoded, "fc5")
    d_fc4 = decode_fc_sigmoid(d_fc5, "fc4")
    d_fc3 = decode_fc_sigmoid(d_fc4, "fc3")
    d_fc2 = decode_fc_sigmoid(d_fc3, "fc2")
    d_fc1 = decode_fc_sigmoid(d_fc2, "fc1")
    reshaped = tf.reshape(d_fc1, [-1, 96, 1, 32])
    d_pool3 = upsample(reshaped)
    d_conv5 = deconv2d_elu(d_pool3, "conv5", [tf.shape(x)[0], 195, 4, 32], "VALID")
    d_pool2 = upsample(d_conv5, 2)
    d_conv4 = deconv2d_elu(d_pool2, "conv4", [tf.shape(x)[0], 394, 12, 32], "VALID")
    d_conv3 = deconv2d_elu(d_conv4, "conv3", [tf.shape(x)[0], 398, 16, 16], "VALID")
    d_pool1 = upsample(d_conv3)
    d_conv2 = deconv2d_elu(d_pool1, "conv2", [tf.shape(x)[0], 798, 18, 16], "VALID")
    y = deconv2d_elu(d_conv2, "conv1", [tf.shape(x)[0], 800, 20, 1], "VALID")

    return x, encoded, y