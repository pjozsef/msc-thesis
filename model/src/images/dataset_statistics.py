import argparse
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


def show_chart(data):
    fig, axes = plt.subplots(
        2,
        3,
        gridspec_kw={'width_ratios': [1, 1, 1], 'height_ratios': [0.01, 1]},
        figsize=(16, 5))
    print_subplot(axes, 0, data["artist"], "Előadók száma", True)
    print_subplot(axes, 1, data["album"], "Albumok száma")
    print_subplot(axes, 2, data["song"], "Dalok száma")

    fig.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


def print_subplot(axes, i, data, title, show_legend=None):
    axes[0, i].axis('off')
    a = axes[1, i]
    x = [data["classical"], data["electronic"], data["metal"]]
    a.pie(x,
          colors=["blue", "orange", "black"],
          labels=x)
    a.set_title(title)
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)

    if show_legend:
        handles, labels = a.get_legend_handles_labels()
        a.legend(handles, ["Klasszikus", "Elektronikus", "Metál"], loc=2, prop={'size': 9})


def print_topk_artist(df, style=None):
    dataframe = df
    if style:
        dataframe = dataframe.loc[dataframe["style"] == style]
    else:
        style = "all"
    counter = Counter(dataframe["artist"])
    print("Top 5 artists", style, [t[0] for t in counter.most_common(5)])


def artist_info(df):
    df = df.drop_duplicates(subset=["artist"])

    result = {}

    for style in ["classical", "electronic", "metal"]:
        artists = df.loc[df["style"] == style]["artist"].values
        print(style, "artists", artists)
        result[style] = artists.size

    return result


def album_info(df):
    result = {}

    for style in ["classical", "electronic", "metal"]:
        last_song = None

        albums = []
        for album in df.loc[df["style"] == style]["album"].values:
            if album != last_song:
                last_song = album
                albums.append(album)
        print(style, "albums", albums)
        result[style] = len(albums)

    return result


def song_info(df):
    result = {}

    for style in ["classical", "electronic", "metal"]:
        songs = df.loc[df["style"] == style]["song"].values
        print(style, "songs", songs.size)
        result[style] = songs.size
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--chart', action='store_true')
    args = parser.parse_args()

    raw = pd.read_csv(args.input_csv, usecols=["style", "artist", "album", "song"])
    df = raw.drop_duplicates()

    print()

    infos = {
        "artist": artist_info(df),
        "album": album_info(df),
        "song": song_info(df)
    }

    print(infos)

    if args.chart:
        show_chart(infos)

    print_topk_artist(df)
    print_topk_artist(df, "classical")
    print_topk_artist(df, "electronic")
    print_topk_artist(df, "metal")


if __name__ == '__main__':
    main()
