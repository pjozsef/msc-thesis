import argparse
import sys
import time

import numpy as np
import tensorflow as tf

from src.train import proto_parser
from src.train.model import model02

if __name__ == "__main__":
    print("Arguments", sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-data-root', required=True)
    parser.add_argument('--train-data-records', nargs='*', required=True)
    parser.add_argument('--job-dir', required=True)
    parser.add_argument('--take', type=int)
    args = parser.parse_args()
    print("Parsed arguments:", args)

    input_records = [args.train_data_root + "/" + record for record in args.train_data_records]
    print(input_records)

    MODEL_NAME = "model-simple"
    BATCH_SIZE = 256
    PREFETCH_BUFFER = 1000
    SHUFFLE_BUFFER = 1000
    TAKE = args.take
    EPOCH = 40
    LEARNING_RATE = 0.1
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

    x, encoded, y, conv_keep_prob, fc_keep_prob = model02.create_model(tf.nn.elu, tf.nn.elu)
    print("Model created")

    cost = tf.reduce_sum(tf.square(y - x))
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)

    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    tf.summary.image("summary_x", x, max_outputs=3)
    tf.summary.image("summary_y", y, max_outputs=3)
    tf.summary.scalar("summary_cost", cost)
    tf.summary.histogram("summary_cost_hist", cost)

    saver = tf.train.Saver()
    savedModelBuilder = tf.saved_model.builder.SavedModelBuilder(args.job_dir + "/final_model")

    writer = tf.summary.FileWriter(args.job_dir)

    with tf.Session() as sess:
        print("Starting session")
        sess.run(init_op)

        merged_summary = tf.summary.merge_all()

        writer.add_graph(sess.graph)

        savedModelBuilder.add_meta_graph_and_variables(
            sess,
            [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                "model": tf.saved_model.signature_def_utils.predict_signature_def(
                    inputs={"x": x},
                    outputs={"encoded": encoded})
            })

        next_element = iterator.get_next()

        summary = None
        step = 0
        for epoch in range(EPOCH + 1):
            print("Epoch:", epoch)
            epoch_start = time.time()
            sess.run(iterator.initializer, feed_dict={filenames: input_records})
            summary = tf.summary.merge_all()
            total_batch = 0
            total_error = 0
            times_for_mini_batch = []
            times_for_optimizer = []
            while True:
                try:
                    start = time.time()
                    images, dimensions, names = sess.run(next_element)
                    times_for_mini_batch.append(time.time() - start)

                    feed_dict = {x: images, conv_keep_prob: 0.1, fc_keep_prob: 0.5}

                    start = time.time()
                    if epoch % 5 == 0:
                        _, cost_value = sess.run([optimizer, cost], feed_dict)
                        total_error += cost_value
                        total_batch += images.shape[0]
                        if images.shape[0] == BATCH_SIZE:
                            all_summary = sess.run(summary, feed_dict)
                            writer.add_summary(all_summary, step)
                    else:
                        sess.run(optimizer, feed_dict)

                    if images.shape[0] == BATCH_SIZE:
                        step += 1
                    times_for_optimizer.append(time.time() - start)
                except tf.errors.OutOfRangeError:
                    if total_error:
                        print("Mean error for epoch", epoch, ":", (total_error / total_batch))
                    print("Total epoch time:", (time.time() - epoch_start) / 60, "minutes")
                    print("Average times for minibatch: ", np.average(times_for_mini_batch))
                    print("Average times for calculation: ", np.average(times_for_optimizer))
                    break
            saver.save(sess, args.job_dir + '/' + MODEL_NAME + '.ckpt', global_step=epoch)
        savedModelBuilder.save()
