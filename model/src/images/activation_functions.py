import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

ELU = "elu"
RELU = "relu"
TANH = "tanh"
SIGMOID = "sigmoid"
ACTIVATIONS = [SIGMOID, TANH, RELU, ELU]


def print_subplot(i, j, x, y, title):
    a = axes[i, j]
    a.axvline(x=0, color='k')
    a.axhline(y=0, color='k')
    a.plot(x, y)
    a.set_title(title)


start = -10
end = 10
size = 50

x = np.linspace(start, end, size)
ys = {}

for activation_string in ACTIVATIONS:
    tf.reset_default_graph()
    activation_input = tf.placeholder(tf.float32)
    activation = getattr(tf.nn, activation_string)
    output = activation(activation_input)

    with tf.Session() as sess:
        y = sess.run(output, feed_dict={activation_input: x})
        ys[activation_string] = y

fig, axes = plt.subplots(
    2,
    2,
    gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1]},
    figsize=(16, 5))
print_subplot(0, 0, x, ys[SIGMOID], SIGMOID.title())
print_subplot(0, 1, x, ys[TANH], TANH.title())
print_subplot(1, 0, x, ys[RELU], RELU.title())
print_subplot(1, 1, x, ys[ELU], ELU.title())

fig.tight_layout()
plt.show()
