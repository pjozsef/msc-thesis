import argparse

import numpy as np
import sklearn.neighbors as neighbors

import src.infer.csv_parser as csv_parser
import src.infer.percentile_parser as percentile_parser


def find_next_song(current_code, tree, topk):
    distances, indices = tree.query([current_code], k=topk)
    distances = distances[0][1:]
    indices = indices[0][1:]
    percentages = np.divide(distances, np.sum(distances))

    next = np.random.choice(len(distances), p=percentages)
    return indices[next]


def song_info(index, infos):
    separator = "___"
    return infos[index]["style"] \
           + separator + infos[index]["artist"] \
           + separator + infos[index]["album"] \
           + separator + infos[index]["song"] \
           + separator + infos[index]["percentile"]


def matches(song1, song2):
    return song1["artist"] == song2["artist"] and song1["album"] == song2["album"] and song1["song"] == song2["song"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--length', type=int, default=10)
    parser.add_argument('--topk', type=int, default=3)
    parser.add_argument('--percentiles')
    args = parser.parse_args()
    if args.percentiles:
        args.percentiles = percentile_parser.parse_percentiles(args.percentiles)
    args.topk += 1
    print(args)

    codes, infos = csv_parser.parse(args.input, args.percentiles)
    tree = neighbors.KDTree(codes, leaf_size=32)
    high = len(codes) - 1
    current_index = np.random.randint(0, high)
    current_code = codes[current_index]
    print(song_info(current_index, infos))
    for i in range(args.length):
        current_index = find_next_song(current_code, tree, args.topk)
        current_code = codes[current_index]
        current_info = infos[current_index]
        print(song_info(current_index, infos))

        delete_indices = []

        for info_index, info in enumerate(infos):
            if matches(current_info, info):
                delete_indices.append(info_index)

        # print(np.shape(codes))
        # codes = np.delete(codes, delete_indices)
        # infos = np.delete(infos, delete_indices)
        # print(np.shape(codes))
        # print(delete_indices)
        for j in delete_indices[::-1]:
            del infos[j]
            del codes[j]
            # print(j, infos[j])
        tree = neighbors.KDTree(codes, leaf_size=32)


if __name__ == '__main__':
    main()
