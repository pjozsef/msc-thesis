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
    latent = latent_dimensions(df)
    mins = latent.min().values
    maxs = latent.max().values

    row_count = df.shape[0]
    update_step = int(row_count / 10)
    print("Original csv size:", row_count)
    output = args.output_folder + "/fake_" + args.input_csv.split("/")[-1]
    print("Output file:", output)

    info_labels = ['style', 'artist', 'album', 'song', 'percentile']
    encoded_dimensions = [str(i) for i in range(32)]
    fieldnames = info_labels + encoded_dimensions

    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(row_count):
            if i % update_step == 0:
                print("{:.2f}%".format(i / row_count * 100))
            meta_data = df.iloc[[i]][info_labels].values.tolist()[0]
            latent_data = next_random(mins, maxs).tolist()
            data = meta_data + latent_data
            csv_row = dict(zip(fieldnames, data))
            writer.writerow(csv_row)


if __name__ == '__main__':
    main()
