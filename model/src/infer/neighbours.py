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

for i, index in enumerate(indices[0]):
    if i == 0:
        print("Starting point")
    else:
        print("{}. neighbour".format(i))
        print("Distance", distances[0][i])
    print("Index:", index)
    print("Style:", infos[index]['style'])
    print("Artist:", infos[index]['artist'])
    print("Album:", infos[index]['album'])
    print("Song:", infos[index]['song'])
    print("Percentile:", infos[index]['percentile'])
    print()
