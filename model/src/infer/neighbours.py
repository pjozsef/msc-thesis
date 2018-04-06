import argparse

import numpy as np
import sklearn.neighbors as neighbors
from tabulate import tabulate

import src.infer.csv_parser as csv_parser
import src.infer.percentile_parser as percentile_parser

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--topk', type=int, default=3)
parser.add_argument('--percentiles')
parser.add_argument('--start-index', type=int)
args = parser.parse_args()
if args.percentiles:
    args.percentiles = percentile_parser.parse_percentiles(args.percentiles)
print(args)
print()
args.topk = args.topk + 1

codes, infos = csv_parser.parse(args.input, args.percentiles)
tree_kd = neighbors.KDTree(codes, leaf_size=32)
low = 0
high = len(codes) - 1
if args.start_index:
    start_index = args.start_index
else:
    start_index = np.random.randint(0, high)

distances, indices = tree_kd.query([codes[start_index]], k=args.topk)

values = []
for i, index in enumerate(indices[0]):
    values.append([
        i,
        index,
        distances[0][i],
        infos[index]['style'],
        infos[index]['artist'],
        infos[index]['album'],
        infos[index]['song'],
        infos[index]['percentile'],
    ])

print(tabulate(values,
               headers=[
                   'Row',
                   'Index',
                   'Distance',
                   'Style',
                   'Artist',
                   'Album',
                   'Song',
                   'Percentile']))
