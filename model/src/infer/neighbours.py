import argparse

import numpy as np
import sklearn.neighbors as neighbors

import src.infer.csv_parser as csv_parser
import src.infer.percentile_parser as percentile_parser

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--topk', type=int, default=3)
parser.add_argument('--percentiles')
args = parser.parse_args()
if args.percentiles:
    args.percentiles = percentile_parser.parse_percentiles(args.percentiles)
print(args)
args.topk = args.topk + 1

codes, infos = csv_parser.parse(args.input, args.percentiles)
tree_kd = neighbors.KDTree(codes, leaf_size=32)
low = 0
high = len(codes) - 1
random_index = np.random.randint(0, high)
distances, indices = tree_kd.query([codes[random_index]], k=args.topk)
print(indices)
print(distances)
for i in indices[0]:
    print(i)
    t = tuple(codes[i])
    print(infos[i])
