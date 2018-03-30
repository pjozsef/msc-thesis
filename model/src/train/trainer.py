import argparse
import sys
import time

import numpy as np
import tensorflow as tf

from src.train import proto_parser
from src.train.model import model01

if __name__ == "__main__":
    print("Arguments", sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-data-root', required=True)
    parser.add_argument('--train-data-records', nargs='*', required=True)
    parser.add_argument('--cv-data-root', required=True)
    parser.add_argument('--cv-data-records', nargs='*', required=True)
    parser.add_argument('--test-data-root', required=True)
    parser.add_argument('--test-data-records', nargs='*', required=True)
    parser.add_argument('--job-dir', required=True)
    parser.add_argument('--epoch', type=int, default=20)
    parser.add_argument('--take', type=int)
    parser.add_argument('--restore')
    args = parser.parse_args()
    print("Parsed arguments:", args)

    train_records = [args.train_data_root + "/" + record for record in args.train_data_records]
    print("Train records:", train_records)

    cv_records = [args.cv_data_root + "/" + record for record in args.cv_data_records]
    print("CV records:", cv_records)

    test_records = [args.test_data_root + "/" + record for record in args.test_data_records]
    print("Test records:", test_records)

    MODEL_NAME = "model-simple"
    BATCH_SIZE = 256
    PREFETCH_BUFFER = 2500
    SHUFFLE_BUFFER = 2500
    TAKE = args.take
    EPOCH = args.epoch
    LEARNING_RATE = 0.001
    CONV_KEEP_PROB = 0.95
    FC_KEEP_PROB = 0.6
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

    x, encoded, y, conv_keep_prob, fc_keep_prob = model01.create_model(tf.nn.elu, tf.nn.elu)
    print("Model created")

    cost = tf.reduce_sum(tf.square(y - x))
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)

    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    tf.summary.image("summary_x", x, max_outputs=1)
    tf.summary.image("summary_y", y, max_outputs=1)
    tf.summary.scalar("summary_cost", cost)
    tf.summary.histogram("summary_cost_hist", cost)

    saver = tf.train.Saver()
    savedModelBuilder = tf.saved_model.builder.SavedModelBuilder(args.job_dir + "/final_model")

    writer = tf.summary.FileWriter(args.job_dir)

    with tf.Session() as sess:
        print("Starting session")

        if args.restore:
            print("Restoring from", args.restore)
            saver.restore(sess, args.restore)
            print("Model restored")
        else:
            sess.run(init_op)
            print("Model initialized from scratch")

        merged_summary = tf.summary.merge_all()

        writer.add_graph(sess.graph)

        savedModelBuilder.add_meta_graph_and_variables(
            sess,
            [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                "model": tf.saved_model.signature_def_utils.predict_signature_def(
                    inputs={
                        "x": x,
                        'fc_keep_prob': fc_keep_prob,
                        'conv_keep_prob': conv_keep_prob},
                    outputs={"encoded": encoded})
            })

        next_element = iterator.get_next()

        summary = None
        step = 0
        #######################
        #        TRAIN        #
        #######################
        for epoch in range(EPOCH + 1):
            print("Epoch:", epoch)
            epoch_start = time.time()
            sess.run(iterator.initializer, feed_dict={filenames: train_records})
            summary = tf.summary.merge_all()

            times_for_mini_batch = []
            times_for_optimizer = []
            while True:
                try:
                    start = time.time()
                    images, dimensions, names = sess.run(next_element)
                    times_for_mini_batch.append(time.time() - start)

                    start = time.time()
                    sess.run(
                        optimizer,
                        {x: images, conv_keep_prob: CONV_KEEP_PROB, fc_keep_prob: FC_KEEP_PROB})
                    times_for_optimizer.append(time.time() - start)
                except tf.errors.OutOfRangeError:
                    print("Total epoch time:", (time.time() - epoch_start) / 60, "minutes")
                    print("Average times for minibatch: ", np.average(times_for_mini_batch))
                    print("Average times for calculation: ", np.average(times_for_optimizer))

                    ########################
                    #          CV          #
                    ########################
                    if epoch % 5 == 0:
                        print("Running CV")
                        total_batch = 0
                        total_error = 0.0
                        sess.run(iterator.initializer, feed_dict={filenames: cv_records})
                        while True:
                            try:
                                images, dimensions, names = sess.run(next_element)
                                if images.shape[0] == BATCH_SIZE:
                                    cost_cv, all_summary = sess.run(
                                        [cost, summary],
                                        {x: images, conv_keep_prob: 1.0, fc_keep_prob: 1.0})
                                    writer.add_summary(all_summary, step)
                                    total_batch += 1
                                    total_error += cost_cv
                                    step += 1
                            except tf.errors.OutOfRangeError:
                                print("Mean CV error for epoch", epoch, ":", (total_error / total_batch))
                                break
                    break
            saver.save(sess, args.job_dir + '/' + MODEL_NAME + '.ckpt', global_step=epoch)
        savedModelBuilder.save()

        ########################
        #         TEST         #
        ########################
        print("Running TEST")
        total_batch = 0
        total_error = 0.0
        sess.run(iterator.initializer, feed_dict={filenames: test_records})
        while True:
            try:
                images, dimensions, names = sess.run(next_element)
                cost_test = sess.run(cost, {x: images, conv_keep_prob: 1.0, fc_keep_prob: 1.0})
                total_batch += 1
                total_error += cost_test
                step += 1
            except tf.errors.OutOfRangeError:
                print("Final TEST error", ":", (total_error / total_batch))
                break
