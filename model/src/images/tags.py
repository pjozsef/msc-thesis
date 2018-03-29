import argparse

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def select_style(df, style):
    return df.loc[df['category'] == style]


def sum(df, style):
    return select_style(df, style)["count"].sum()


def max(df, style):
    return select_style(df, style)["count"].max()


def color_for(row, m):
    style, tag, count = row
    if style == "classical":
        return matplotlib.colors.hsv_to_rgb([0.6, count / m, 0.8])
    elif style == "electronic":
        return matplotlib.colors.hsv_to_rgb([0.15, count / m, 0.8])
    elif style == "metal":
        return matplotlib.colors.hsv_to_rgb([0.0, 0, 1 - (count / m)])
    else:
        raise Exception("Unrecognized style: " + style)


def print_plot(i, df, style):
    m = max(df, style)
    filtered = select_style(df, style)
    colors = []
    for index, row in filtered.iterrows():
        colors.append(color_for(row, m))

    plt.pie([1], colors=["black"])
    filtered['count'].plot.pie(labels=filtered["tag"], fontsize=8, colors=colors, figsize=(6, 6), legend=None)
    plt.axis('off')
    plt.title(style.capitalize())
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--input-csv', required=True)
args = parser.parse_args()

df = pd.read_csv(args.input_csv).sort_values(by=['category', 'count'])
color_map = {
    "classical": matplotlib.colors.hsv_to_rgb([0.6, 1, 0.8]),
    "electronic": matplotlib.colors.hsv_to_rgb([0.1, 1, 0.8]),
    "metal": matplotlib.colors.hsv_to_rgb([0.6, 0, 0.8])
}

########################################
# ###########3 categories############# #
########################################

total_classical = sum(df, "classical")
total_electronic = sum(df, "electronic")
total_metal = sum(df, "metal")

plt.pie(
    [total_classical, total_electronic, total_metal],
    labels=["classical", "electronic", "metal"],
    colors=["blue", "orange", "black"])
plt.title("Zenei stílusok eloszlása")
plt.show()

########################################
# ########separate categories######### #
########################################
print_plot(0, df, "classical")
print_plot(1, df, "electronic")
print_plot(2, df, "metal")
