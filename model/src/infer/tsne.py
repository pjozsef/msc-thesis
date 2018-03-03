import argparse
import csv
import time

import matplotlib.colors
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--percentiles', nargs='*')
parser.add_argument('--perplexity', required=True, type=int)
args = parser.parse_args()
print(args)

header = None
infos = []
codes = []
with open(args.input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
        if args.percentiles:
            percentile = row[4]
            if percentile in args.percentiles:
                infos.append(row[0:5])
                codes.append(row[5:37])
        else:
            infos.append(row[0:5])
            codes.append(row[5:37])

start = time.time()
# 5 30 50 100
tsne = TSNE(learning_rate=10, n_iter=15000, perplexity=args.perplexity)
codes_2d = tsne.fit_transform(codes)
print("Iterations run:", tsne.n_iter_, "/", tsne.n_iter)
print("Divergence:", tsne.kl_divergence_)
print("T-SNE finished in", time.time() - start, "seconds")

x = codes_2d[:, 0]
y = codes_2d[:, 1]
label = []
labelMapping = {
    'classical': 0,
    'electronic': 1,
    'metal': 2
}
for info in infos:
    label.append(labelMapping[info[0]])

alpha = 0.5
colorMapping = {
    0: matplotlib.colors.to_rgba('blue', alpha=alpha),
    1: matplotlib.colors.to_rgba('orange', alpha=alpha),
    2: matplotlib.colors.to_rgba('black', alpha=alpha)
}
colors = [colorMapping[style] for style in label]
fig = plt.figure(figsize=(8, 8))
plt.scatter(x, y, c=colors)
plt.title("Perplexity: " + str(args.perplexity))
plt.show()
