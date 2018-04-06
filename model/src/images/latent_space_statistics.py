import argparse

import matplotlib.pyplot as plt
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


def area(df, style=None, artist=None, song=None, percentile=None, sort=None):
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
    df = latent_dimensions(df)
    df = df - df.min()
    df = df.divide(df.sum(axis=1), axis=0)

    area = df.plot.area(legend=None)
    area.set_title(array_as_string([style, artist, song, percentile]))


def main():
    pd.set_option('display.expand_frame_repr', False)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    # describe = df.describe()
    # print(describe)
    # print()
    # print(describe.transpose())
    # plt.imshow(describe, cmap='hot', interpolation='none')
    # plt.yticks(np.arange(0.5, len(describe.index), 1), describe.index)
    # plt.xticks(np.arange(0.5, len(describe.columns), 1), describe.columns)
    # plt.show()

    # boxplot(latent_dimensions(df), "Teljes látens tér")
    # boxplot(latent_dimensions(filter_style(df, CLASSICAL)), "Látens tér klasszikus része")
    # boxplot(latent_dimensions(filter_style(df, ELECTRONIC)), "Látens tér elektronikus része")
    # boxplot(latent_dimensions(filter_style(df, METAL)), "Látens tér metál része")

    # area(df, artist="Arch Enemy", song="The Day You Died")
    # area(df, artist="Arch Enemy", song="Taking Back My Soul")
    # area(df, artist="Arch Enemy", song="Nemesis")
    # area(df, artist="Christophe Beck", song="Let It Go")
    # area(df, artist="Juno Reactor", song="Navras")

    # plt.matshow(latent_dimensions(filter_percentile(df, 50)).corr())

    # pd.plotting.scatter_matrix(
    #     latent_dimensions(filter_percentile(df, 75))
    #     , alpha=0.2, figsize=(32, 32), diagonal='kde')

    # columns = ["style"] + [str(i) for i in range(32)]
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
