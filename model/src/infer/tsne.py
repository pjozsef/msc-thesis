import argparse
import time

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE


def parse_data(args):
    info_labels = ['style', 'artist', 'album', 'song', 'percentile']
    encoded_dimensions = [str(j) for j in range(32)]

    df = pd.read_csv(args.input)
    print("Dataframe original size:", df.shape[0])
    if args.percentiles:
        df = df[df['percentile'].isin(args.percentiles)]
        print("Dataframe size after percentile filtering:", df.shape[0])
    if args.sample:
        classical = df[df['style'] == 'classical'].sample(n=args.sample, random_state=args.seed)
        electronic = df[df['style'] == 'electronic'].sample(n=args.sample, random_state=args.seed)
        metal = df[df['style'] == 'metal'].sample(n=args.sample, random_state=args.seed)
        df = pd.concat([classical, electronic, metal])
        print("Dataframe size after sampling:", df.shape[0])

    return df[info_labels].values.tolist(), df[encoded_dimensions].values.tolist()


def create_embeddings(codes, perplexites=None, retries=3):
    if perplexites is None:
        perplexites = [30, 50, 100]
    embeddings = []
    for perplexity in perplexites:
        divergence_map = {}
        divergences = []
        for retry in range(retries):
            tsne_result = do_tsne(codes, perplexity)
            divergence = tsne_result['kldiv']
            divergence_map[divergence] = tsne_result
            divergences.append(divergence)
        min_div = np.min(divergences)
        embeddings.append(divergence_map[min_div])
    return embeddings


def do_tsne(codes, perplexity, iterations=15000, lr=100):
    start = time.time()
    tsne = TSNE(learning_rate=lr, n_iter=iterations, perplexity=perplexity)
    codes_2d = tsne.fit_transform(codes)
    print()
    print("Perplexity:", perplexity)
    print("Iterations run:", tsne.n_iter_, "/", tsne.n_iter)
    print("Divergence:", tsne.kl_divergence_)
    print("T-SNE finished in", time.time() - start, "seconds")
    return {'perplexity': perplexity, "kldiv": tsne.kl_divergence_, "embedding": codes_2d}


def save_and_show_plot(embeddings, colors):
    fig, axes = plt.subplots(
        2,
        len(embeddings),
        gridspec_kw={'width_ratios': [1, 1, 1], 'height_ratios': [0.01, 1]},
        figsize=(16, 5))
    plt.suptitle(args.title)
    for i in range(len(embeddings)):
        embedding = embeddings[i]
        x = embedding['embedding'][:, 0]
        y = embedding['embedding'][:, 1]
        axes[0, i].axis('off')
        a = axes[1, i]
        a.scatter(x, y, c=colors, s=20)
        title = "Perplexity: {}\nKL Divergence: {:0.4f}".format(embedding['perplexity'], embedding['kldiv'])
        a.set_title(title)
        a.get_xaxis().set_visible(False)
        a.get_yaxis().set_visible(False)
    fig.tight_layout()
    if args.save:
        plt.savefig(args.save + args.title + '.png')
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--percentiles')
parser.add_argument('--title', required=True)
parser.add_argument('--save')
parser.add_argument('--retries', type=int, default=1)
parser.add_argument('--sample', type=int)
parser.add_argument('--seed', type=int)
args = parser.parse_args()
if args.seed:
    np.random.seed(args.seed)
if args.percentiles:
    all_percentiles = []
    for percentile in args.percentiles.split(","):
        if percentile.isdigit():
            all_percentiles.append(percentile)
        else:
            start, end = percentile.split("-")
            start = int(start)
            end = int(end)
            for i in range(start, end + 1):
                all_percentiles.append(str(i))
    args.percentiles = all_percentiles
print(args)

infos, codes = parse_data(args)

label = []
labelMapping = {
    'classical': 0,
    'electronic': 1,
    'metal': 2
}
for info in infos:
    label.append(labelMapping[info[0]])

alpha = 0.2
colorMapping = {
    0: matplotlib.colors.to_rgba('blue', alpha=alpha),
    1: matplotlib.colors.to_rgba('orange', alpha=alpha),
    2: matplotlib.colors.to_rgba('black', alpha=alpha)
}
colors = [colorMapping[style] for style in label]

embeddings = create_embeddings(codes, retries=args.retries)
save_and_show_plot(embeddings, colors)
