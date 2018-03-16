import argparse
import configparser
import csv
import glob
import json
import time
from collections import Counter

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--input-folder', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    apikey = config['credentials']['apikey']
    secret = config['credentials']['secret']

    paths = glob.glob(args.input_folder)
    raw_artists = [p.split("/")[-1].split("__")[1] for p in paths]
    artist_count = Counter(raw_artists)
    artists = set(raw_artists)
    errors = []
    keys = ["artist", "count", "tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]

    with open(args.output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for i, artist in enumerate(artists):
            count = artist_count[artist]
            print(i, "/", len(artists), artist, count)
            url = "http://ws.audioscrobbler.com/2.0/" \
                  "?method=artist.getinfo" \
                  "&autocorrect=1" \
                  "&format=json" \
                  "&artist={}" \
                  "&api_key={}".format(artist, apikey)
            r = requests.get(url)
            response = json.loads(r.text)
            if "error" not in response:
                values = [artist, count]
                for tag in response["artist"]['tags']["tag"]:
                    values.append(tag["name"])
                csv_row = dict(zip(keys, values))
                writer.writerow(csv_row)
            else:
                print("Error with:", artist, count)
                errors.append({artist: count})
            time.sleep(0.2)
    if errors:
        print("Could not get info:", errors)


if __name__ == '__main__':
    main()
