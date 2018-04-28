import argparse
from math import pi

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PERCENTILE = 'percentile'
STYLE = 'style'
ARTIST = 'artist'
SONG = 'song'


def prefilter(df, style=None, artist=None, song=None, percentile=None, sort=None):
    if percentile:
        df = df.loc[df[PERCENTILE] >= percentile]
    if style:
        df = df.loc[df[STYLE] == style]
    if artist:
        df = df.loc[df[ARTIST] == artist]
    if song:
        df = df.loc[df[SONG] == song]
    if sort:
        df = df.sort_values(by=sort).reset_index()
    return df


def latent_dimensions(df):
    return df[[str(i) for i in range(32)]]


def radar_song(df, export_folder, style=None, artist=None, song=None, percentile=None, sort=None):
    plt.figure()
    df = prefilter(df, style, artist, song, percentile, sort)
    style = df[STYLE].drop_duplicates().values[0]
    df = latent_dimensions(df)
    dimension_sums = latent_dimensions(df).sum()
    dimension_sums = dimension_sums - dimension_sums.min()

    categories = list(df)
    N = len(categories)
    values = dimension_sums.tolist()
    values += values[:1]
    values = np.array(values)
    values = np.divide(values, values.max()).tolist()

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], [], color="grey", size=7)
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)
    title = "{} - {} - {} - {}-100 percentilisek".format(style, artist, song, percentile)
    ax.set_title(title)
    plt.savefig(export_folder + "/" + title.replace(" ", "_") + '.png')
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--artists', required=True)
    parser.add_argument('--export-folder', required=True)
    args = parser.parse_args()
    args.artists = [a.strip() for a in args.artists.split(",")]
    print(args.artists)

    df = pd.read_csv(args.input_csv)
    df = df[df[ARTIST].isin(args.artists)]

    artist_songs = df[[ARTIST, SONG]]
    artist_songs = artist_songs.drop_duplicates()

    for i in artist_songs.values:
        print(i)
        radar_song(df, args.export_folder, artist=i[0], song=i[1], percentile=15)


if __name__ == '__main__':
    main()
