import tensorflow as tf

weights = {}


def initializer():
    return tf.contrib.layers.xavier_initializer(uniform=False)


def bias_initializer():
    return tf.constant_initializer(0.0)


def conv2d(previous_layer, kernel_size, layer_scope, activation_function, keep_prob, padding="SAME"):
    with tf.variable_scope(layer_scope):

        kernel = tf.get_variable(
            name='kernel',
            shape=kernel_size,
            initializer=initializer())
        global weights
        weights[layer_scope] = kernel

        bias = tf.get_variable(
            name="bias",
            shape=[kernel_size[-1]],
            initializer=bias_initializer())
        convolution = tf.nn.conv2d(
            input=previous_layer,
            filter=kernel,
            strides=[1, 1, 1, 1],
            padding=padding)
        convolution_with_bias = tf.nn.bias_add(
            value=convolution,
            bias=bias)
        convolution_with_bias = tf.nn.dropout(convolution_with_bias, keep_prob)
        activation = activation_function(convolution_with_bias, name="activation")

        tf.summary.histogram("summary_weights", kernel)
        tf.summary.histogram("summary_activations", activation)

        return activation


def deconv2d(previous_layer, layer_scope, output_shape, activation_function, padding="SAME"):
    with tf.variable_scope("decode_" + layer_scope):
        global weights
        kernel = weights[layer_scope]
        bias = tf.get_variable(
            name="bias",
            shape=[kernel.shape[2]],
            initializer=bias_initializer())
        deconvolution = tf.nn.conv2d_transpose(
            value=previous_layer,
            filter=kernel,
            output_shape=output_shape,
            strides=[1, 1, 1, 1],
            padding=padding)
        deconvolution_with_bias = tf.nn.bias_add(
            value=deconvolution,
            bias=bias)
        return activation_function(deconvolution_with_bias)


def maxpool(previous_layer, kernel_size=None):
    if isinstance(kernel_size, int):
        kernel_size = [kernel_size, kernel_size]
    if kernel_size is None:
        kernel_size = [2, 1]

    height = kernel_size[0]
    width = kernel_size[1]
    return tf.nn.max_pool(
        value=previous_layer,
        ksize=[1, height, width, 1],
        strides=[1, height, width, 1],
        padding='VALID')


def upsample(previous_layer, kernel_size=None):
    if isinstance(kernel_size, int):
        kernel_size = [kernel_size, kernel_size]
    if kernel_size is None:
        kernel_size = [2, 1]

    height_multiplier = kernel_size[0]
    width_multiplier = kernel_size[1]
    new_height = previous_layer.shape[1] * height_multiplier
    new_width = previous_layer.shape[2] * width_multiplier

    return tf.image.resize_images(
        previous_layer,
        [new_height, new_width],
        method=tf.image.ResizeMethod.NEAREST_NEIGHBOR
    )


def flatten(previous_layer):
    dim = tf.reduce_prod(tf.shape(previous_layer)[1:])
    return tf.reshape(previous_layer, [-1, dim])


def fc(previous_layer, weight_size, activation_function, keep_prob, layer_scope, layer_name=None):
    with tf.variable_scope(layer_scope):

        input_size = weight_size[0]
        output_size = weight_size[1]
        weight = tf.get_variable(
            name='weight',
            shape=[input_size, output_size],
            initializer=initializer())
        global weights
        weights[layer_scope] = weight

        bias = tf.get_variable(
            name='bias',
            shape=[output_size],
            dtype=tf.float32,
            initializer=bias_initializer())

        h = tf.nn.bias_add(
            name='h',
            value=tf.matmul(previous_layer, weight),
            bias=bias)

        h = tf.nn.dropout(h, keep_prob)

        activation = activation_function(h, name=layer_name)
        # tf.summary.image("summary_weights_img", tf.reshape(weights, [1, weight_size[0], weight_size[1], 1]))
        tf.summary.histogram("summary_weights", weight)
        tf.summary.histogram("summary_activations", activation)

        return activation


def decode_fc(previous_layer, activation_function, layer_scope):
    with tf.variable_scope("decode_" + layer_scope):
        global weights
        weight = tf.transpose(weights[layer_scope])

        bias = tf.get_variable(
            name='bias',
            shape=[weight.shape[1]],
            dtype=tf.float32,
            initializer=bias_initializer())

        h = tf.nn.bias_add(
            name='h',
            value=tf.matmul(previous_layer, weight),
            bias=bias)

        return activation_function(h)
