import csv


def parse(csv_path, percentiles=None):
    with open(csv_path, 'r') as csvfile:
        infos = []
        codes = []
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            if percentiles:
                percentile = row[4]
                if percentile in percentiles:
                    code = row[5:37]
                    info = {
                        "style": row[0],
                        "artist": row[1],
                        "album": row[2],
                        "song": row[3],
                        "percentile": row[4]
                    }
                    infos.append(info)
                    codes.append(code)
            else:
                code = row[5:37]
                info = {
                    "style": row[0],
                    "artist": row[1],
                    "album": row[2],
                    "song": row[3],
                    "percentile": row[4]
                }
                infos.append(info)
                codes.append(code)
        return codes, infos
