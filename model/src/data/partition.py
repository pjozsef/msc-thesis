import argparse
import glob
import random
from collections import defaultdict

import numpy as np


def collect_by_percentiles(paths):
    result = defaultdict(list)
    for p in paths:
        percentile = int(p.split("__")[-1][:-4])
        result[percentile].append(p)
    return result


def group_by_sets(paths_by_percentile, cv_ratio, test_ratio):
    total_train = []
    total_cv = []
    total_test = []
    for percentile, paths in paths_by_percentile.items():
        current = np.array(paths)
        random.shuffle(current)
        current = current.tolist()
        length = len(current)
        until = int(length * cv_ratio)
        cv = current[0:until]

        current = [x for x in current if x not in cv]
        until = int(length * test_ratio)
        test = current[0:until]

        train = [x for x in current if x not in test]

        total_train = total_train + train
        total_cv = total_cv + cv
        total_test = total_test + test

    print("total train size:", len(total_train))
    print("total cv size:", len(total_cv))
    print("total test size:", len(total_test))
    return {
        "train": total_train,
        "cv": total_cv,
        "test": total_test
    }


def export_partition(partitionDict):
    for file_name, partition in partitionDict.items():
        with open("{}/{}_{}.txt".format(args.output_dir, args.output_file, file_name), "w") as file:
            for song in partition:
                file.write(song + "\n")


parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--output-file', required=True)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--train', type=float, default=0.6)
parser.add_argument('--cv', type=int, default=0.2)
parser.add_argument('--test', type=int, default=0.2)
parser.add_argument('--output-dir', default=".")
args = parser.parse_args()

ratio_sum = args.train + args.cv + args.test
assert ratio_sum == 1.0, "Train, CV and test data ratio must add up to 1.0, but was {}.".format(ratio_sum)
print(args)

np.random.seed(args.seed)
paths = glob.glob(args.source)
partitionDict = group_by_sets(collect_by_percentiles(paths), args.cv, args.test)
export_partition(partitionDict)
