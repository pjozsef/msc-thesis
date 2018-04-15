import argparse
import csv

import numpy as np
import pandas as pd


def latent_dimensions(df):
    return df[[str(i) for i in range(32)]]


def next_random(mins, maxs):
    uniform = np.random.random(mins.size)
    range = maxs - mins
    return (uniform * range) + mins


def main():
    pd.set_option('display.expand_frame_repr', False)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--output-folder', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    df = latent_dimensions(df)
    mins = df.min().values
    maxs = df.max().values

    style_count = int(df.size / 3)
    update_step = int(style_count / 10)
    print("Original csv size:", df.size)
    print("Size per styles:", df.size / 3)
    output = args.output_folder + "/fake_" + args.input_csv.split("/")[-1]
    print("Output file:", output)

    info_labels = ['style', 'artist', 'album', 'song', 'percentile']
    encoded_dimensions = [str(i) for i in range(32)]
    fieldnames = info_labels + encoded_dimensions

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for style in ["classical", "electronic", "metal"]:
            print("Starting", style)
            for i in range(style_count):
                if i % update_step == 0:
                    print("{:.2f}%".format(i / style_count * 100))
                meta_data = [style, "fake_artist", "fake_album", "fake_song", 100]
                latent_data = next_random(mins, maxs).tolist()
                data = meta_data + latent_data
                csv_row = dict(zip(fieldnames, data))
                writer.writerow(csv_row)


if __name__ == '__main__':
    main()
