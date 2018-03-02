import argparse
import csv
import time

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=TSNE)
args = parser.parse_args()

header = None
infos = []
codes = []
with open(args.input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
        if row[4] == '75':
            infos.append(row[0:5])
            codes.append(row[5:37])

start = time.time()
tsne = TSNE(learning_rate=200, n_iter=5000, perplexity=50)
codes_2d = tsne.fit_transform(codes)
print("Iterations:", tsne.n_iter)
print("Iterations:", tsne.n_iter_)
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

colorMapping = {
    0: 'blue',
    1: 'orange',
    2: 'black'
}
colors = [colorMapping[style] for style in label]
fig = plt.figure(figsize=(8, 8))
plt.scatter(x, y, c=colors)
plt.show()
