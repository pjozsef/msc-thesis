import argparse

import numpy as np
import sklearn.neighbors as neighbors
from tabulate import tabulate

import src.infer.csv_parser as csv_parser
import src.infer.percentile_parser as percentile_parser


def get_percentages(distances):
    reciprocal = np.reciprocal(distances)
    return reciprocal / np.sum(reciprocal)


def find_next_song(current_code, tree, topk):
    distances, indices = tree.query([current_code], k=topk)
    distances = distances[0][1:]
    indices = indices[0][1:]

    percentages = get_percentages(distances)

    next = np.random.choice(len(distances), p=percentages)
    return indices[next]


def song_info(index, infos, row):
    return [
        row,
        index,
        infos[index]["style"],
        infos[index]["artist"],
        infos[index]["album"],
        infos[index]["song"],
        infos[index]["percentile"]
    ]


def matches(song1, song2):
    return song1["artist"] == song2["artist"] and song1["album"] == song2["album"] and song1["song"] == song2["song"]


def remove_current_song(codes, infos, current_info):
    delete_indices = []

    for info_index, info in enumerate(infos):
        if matches(current_info, info):
            delete_indices.append(info_index)

    for j in delete_indices[::-1]:
        del infos[j]
        del codes[j]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--length', type=int, default=10)
    parser.add_argument('--topk', type=int, default=3)
    parser.add_argument('--percentiles')
    parser.add_argument('--start-index', type=int)
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()
    if args.percentiles:
        args.percentiles = percentile_parser.parse_percentiles(args.percentiles)
    if args.seed:
        np.random.seed(args.seed)
    args.topk += 1
    print(args)

    codes, infos = csv_parser.parse(args.input, args.percentiles)
    max_index = len(codes) - 1
    if args.start_index:
        current_index = args.start_index
    else:
        current_index = np.random.randint(0, max_index)
    current_code = codes[current_index]

    row = 0
    header = ["Row", "Index", "Style", "Artist", "Album", "Song", "Percentile"]
    values = [song_info(current_index, infos, row)]
    remove_current_song(codes, infos, infos[current_index])
    tree = neighbors.KDTree(codes, leaf_size=32)

    for i in range(args.length):
        current_index = find_next_song(current_code, tree, args.topk)
        current_code = codes[current_index]
        current_info = infos[current_index]
        values.append(song_info(current_index, infos, row))

        remove_current_song(codes, infos, current_info)
        tree = neighbors.KDTree(codes, leaf_size=32)
        row += 1
    print(tabulate(values, headers=header))


if __name__ == '__main__':
    main()
