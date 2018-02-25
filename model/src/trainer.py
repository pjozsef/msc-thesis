import argparse
import sys
import time

import numpy as np
import tensorflow as tf

from src import model_simple01
from src import proto_parser

if __name__ == "__main__":
    print("Arguments", sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-data-root', required=True)
    parser.add_argument('--train-data-records', nargs='*', required=True)
    parser.add_argument('--job-dir', required=True)
    args = parser.parse_args()
    print("Parsed arguments:", args)

    input_records = [args.train_data_root + "/" + record for record in args.train_data_records]
    print(input_records)

    BATCH_SIZE = 32
    PREFETCH_BUFFER = 1000
    SHUFFLE_BUFFER = 1000
    TAKE = None
    EPOCH = 30
    LEARNING_RATE = 0.01
    print("Batch size:", BATCH_SIZE)
    print("Prefetch buffer:", PREFETCH_BUFFER)
    print("Shuffle buffer:", SHUFFLE_BUFFER)
    print("Take:", TAKE)
    print("Epoch count:", EPOCH)
    print("Learning rate:", LEARNING_RATE)

    filenames = tf.placeholder(tf.string, shape=[None])
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.shuffle(buffer_size=SHUFFLE_BUFFER)
    dataset = dataset.map(proto_parser.parse_proto)
    dataset = dataset.prefetch(PREFETCH_BUFFER)
    dataset = dataset.batch(BATCH_SIZE)
    if TAKE:
        dataset = dataset.take(TAKE)
    print("Dataset initialized")

    iterator = dataset.make_initializable_iterator()

    x, encoded, y = model_simple01.create_model()
    print("Model created")

    cost = tf.reduce_sum(tf.square(y - x))
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)

    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    saver = tf.train.Saver()

    with tf.Session() as sess:
        print("Starting session")
        sess.run(init_op)
        next_element = iterator.get_next()

        for epoch in range(EPOCH):
            print("Epoch:", epoch)
            sess.run(iterator.initializer, feed_dict={filenames: input_records})
            total_batch = 0
            total_error = 0
            times_for_mini_batch = []
            times_for_optimizer = []
            while True:
                try:
                    start = time.time()
                    images, dimensions, names = sess.run(next_element)
                    times_for_mini_batch.append(time.time() - start)

                    start = time.time()
                    if epoch % 5 == 0:
                        _, cost_value = sess.run([optimizer, cost], feed_dict={x: images})
                        total_error += cost_value
                        total_batch += images.shape[0]
                    else:
                        sess.run(optimizer, feed_dict={x: images})
                    times_for_optimizer.append(time.time() - start)
                except tf.errors.OutOfRangeError:
                    if total_error:
                        print("Mean error for epoch", epoch, ":", (total_error / total_batch))
                    print("Average times for minibatch: ", np.average(times_for_mini_batch))
                    print("Average times for calculation: ", np.average(times_for_optimizer))
                    break
            saver.save(sess, args.job_dir + "/model_simple", global_step=epoch)
