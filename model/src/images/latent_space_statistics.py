import argparse
from math import pi

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PERCENTILE = 'percentile'
STYLE = 'style'
ARTIST = 'artist'
SONG = 'song'

CLASSICAL = "classical"
ELECTRONIC = "electronic"
METAL = "metal"

SAMPLE_SIZE = 300
ALPHA = 0.1


def array_as_string(arr):
    return " - ".join([str(x) for x in arr if x is not None])


def latent_dimensions(df):
    return df[[str(i) for i in range(32)]]


def filter_style(df, style):
    return df.loc[df[STYLE] == style]


def filter_percentile(df, percentile):
    return df.loc[df[PERCENTILE] >= percentile]


def boxplot(df, title=None):
    plt.figure()
    bp = df.boxplot(showfliers=False)
    if title:
        bp.set_title(title)


def prefilter(df, style=None, artist=None, song=None, percentile=None, sort=None):
    if percentile:
        df = filter_percentile(df, percentile)
    if style:
        df = filter_style(df, style)
    if artist:
        df = df.loc[df[ARTIST] == artist]
    if song:
        df = df.loc[df[SONG] == song]
    if sort:
        df = df.sort_values(by=sort).reset_index()
    return df


def area(df, style=None, artist=None, song=None, percentile=None, sort=None):
    df = prefilter(df, style, artist, song, percentile, sort)
    df = latent_dimensions(df)
    df = df - df.min()
    df = df.divide(df.sum(axis=1), axis=0)

    area = df.plot.area(legend=None)
    area.set_title(array_as_string([style, artist, song, percentile]))


def pie_song(df, style=None, artist=None, song=None, percentile=None, sort=None):
    plt.figure()
    df = prefilter(df, style, artist, song, percentile, sort)
    dimension_sums = latent_dimensions(df).sum()
    dimension_sums = dimension_sums - dimension_sums.min()
    pie = dimension_sums.plot.pie()
    pie.set_title(array_as_string([style, artist, song, percentile]))


def radar_song(df, style=None, artist=None, song=None, percentile=None, sort=None):
    plt.figure()
    df = prefilter(df, style, artist, song, percentile, sort)
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
    ax.set_title(array_as_string([style, artist, song, str(percentile) + "-100"]))


def main():
    pd.set_option('display.expand_frame_repr', False)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    latent = latent_dimensions(df)

    # boxplot(latent_dimensions(df), "Teljes látens tér")
    # boxplot(latent_dimensions(filter_style(df, CLASSICAL)), "Látens tér klasszikus stílushoz tartozó altere")
    # boxplot(latent_dimensions(filter_style(df, ELECTRONIC)), "Látens tér elektronikus stílushoz tartozó altere")
    # boxplot(latent_dimensions(filter_style(df, METAL)), "Látens tér metál stílushoz tartozó altere")

    # area(df, artist="Arch Enemy", song="The Day You Died")
    # area(df, artist="Arch Enemy", song="Taking Back My Soul")
    # area(df, artist="Arch Enemy", song="Nemesis")
    # area(df, artist="Christophe Beck", song="Let It Go")
    # area(df, artist="Juno Reactor", song="Navras")

    # pie_song(df, artist="Arch Enemy", song="The Day You Died", percentile=50)
    # pie_song(df, artist="Arch Enemy", song="Taking Back My Soul", percentile=50)
    # pie_song(df, artist="Arch Enemy", song="Nemesis", percentile=50)
    # pie_song(df, artist="Christophe Beck", song="Let It Go", percentile=50)
    # pie_song(df, artist="Juno Reactor", song="Navras", percentile=50)

    # radar_song(df, artist="Arch Enemy", song="The Day You Died", percentile=50)
    # radar_song(df, artist="Arch Enemy", song="Taking Back My Soul", percentile=50)
    # radar_song(df, artist="Arch Enemy", song="Nemesis", percentile=50)
    # radar_song(df, artist="Christophe Beck", song="Let It Go", percentile=50)
    # radar_song(df, artist="Rammstein", song="Feuer Frei!", percentile=50)
    # radar_song(df, artist="Juno Reactor", song="Navras", percentile=50)

    # plt.matshow(latent_dimensions(filter_percentile(df, 50)).corr())

    # pd.plotting.scatter_matrix(
    #     latent_dimensions(filter_percentile(df, 75))
    #     , alpha=0.2, figsize=(32, 32), diagonal='kde')

    columns = ["style"] + [str(i) for i in range(32)]
    # base_df = filter_percentile(df, 75)[columns]
    # classical_df = base_df.loc[base_df[STYLE] == CLASSICAL].sample(SAMPLE_SIZE)
    # electronic_df = base_df.loc[base_df[STYLE] == ELECTRONIC].sample(SAMPLE_SIZE)
    # metal_df = base_df.loc[base_df[STYLE] == METAL].sample(SAMPLE_SIZE)
    # merged_df = metal_df.append(electronic_df).append(classical_df)
    # pd.plotting.parallel_coordinates(merged_df, 'style', color=[
    #     matplotlib.colors.to_rgba('blue', alpha=ALPHA),
    #     matplotlib.colors.to_rgba('orange', alpha=ALPHA),
    #     matplotlib.colors.to_rgba('black', alpha=ALPHA)
    # ])

    # pd.plotting.andrews_curves(filter_percentile(df, 100)[columns], 'style', color=[
    #     matplotlib.colors.to_rgba('blue', alpha=0.1),
    #     matplotlib.colors.to_rgba('orange', alpha=0.1),
    #     matplotlib.colors.to_rgba('black', alpha=0.1)
    # ])

    # plt.figure()
    # pd.plotting.lag_plot(latent_dimensions(filter_percentile(df, 100)))
    # plt.figure()
    # pd.plotting.lag_plot(latent_dimensions(filter_style(filter_percentile(df, 100), CLASSICAL)))
    # plt.figure()
    # pd.plotting.lag_plot(latent_dimensions(filter_style(filter_percentile(df, 100), ELECTRONIC)))
    # plt.figure()
    # pd.plotting.lag_plot(latent_dimensions(filter_style(filter_percentile(df, 100), METAL)))

    # latent_dimensions(filter_percentile(df, 100)).diff().hist(bins=50)

    plt.show()


if __name__ == '__main__':
    main()
