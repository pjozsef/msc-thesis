import argparse
import csv
from collections import Counter

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--output-csv', required=True)
    args = parser.parse_args()

    tags = []
    blacklist = ['', 'seen live', 'mistagged artist', 'unknown', 'under 2000 listeners', 'rapcore', "hip-hop", 'german',
                 'finnish', 'swedish', 'hungarian', 'all', 'female vocalists', 'video game music', 'japanese',
                 'mysterious', 'indie', 'hip-hop', 'shoegaze']
    classical = "classical"
    metal = "metal"
    electronic = "electronic"
    category_map = {
        'industrial': electronic,
        'soundtrack': classical,
        'dark ambient': electronic,
        'darkwave': electronic,
        'gothic': metal,
        'electronic': electronic,
        'melodic death metal': metal,
        'black metal': metal,
        'classical': classical,
        'ebm': electronic,
        'industrial metal': metal,
        'symphonic metal': metal,
        'folk metal': metal,
        'dark electro': electronic,
        'hardcore': electronic,
        'metal': metal,
        'psytrance': electronic,
        'love metal': metal,
        'death metal': metal,
        'nu metal': metal,
        'dubstep': electronic,
        'gothic metal': metal,
        'futurepop': electronic,
        'avant-garde metal': metal,
        'power metal': metal,
        'speedcore': electronic,
        'instrumental': classical,
        'progressive metal': metal,
        'thrash metal': metal,
        'metalcore': metal,
        'rock': metal,
        'orchestra': classical,
        'doom metal': metal,
        'darkpsy': electronic,
        'breakcore': metal,
        'ambient': classical,
        'gothic rock': metal,
        'synthpop': electronic,
        'psychedelic rock': metal,
        'psychedelic': electronic,
        'classica': classical,
        'orchestral': classical,
        'piano': classical,
        'trance': electronic,
        'psychedelic trance': electronic,
        'forest': electronic,
        'acoustic': classical,
        'hard-rock': metal
    }
    unrecognized = []

    with open(args.input_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            count = int(int(row[1]) / 18)
            filtered = [r.lower().strip() for r in row[2:] if r not in blacklist]
            if filtered:
                row_tags = [filtered[0]] * count
                print(row_tags)
                tags += row_tags

    counts = Counter(tags)
    with open(args.output_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["category", "tag", "count"])
        writer.writeheader()
        for pair in counts.most_common():
            tag, count = pair
            if count >= 10 and tag in category_map:
                category = category_map[tag]
                if not category:
                    raise Exception("Cannot find {}".format(tag))
                writer.writerow({"category": category, "tag": tag, "count": count})
            else:
                unrecognized.append(tag)
    if unrecognized:
        print("Unrecognized tags:")
        for item in unrecognized:
            print(item)

    with open(args.output_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        columns = next(reader)
        data = []
        for row in reader:
            category, tag, count = row
            data.append([category, tag, int(count)])
        data_frame = pd.DataFrame(data=data, columns=columns)
        print(data_frame.describe())
        print(data_frame.groupby("category").sum())


if __name__ == '__main__':
    main()
