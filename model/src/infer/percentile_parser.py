def parse_percentiles(raw_percentiles):
    all_percentiles = []
    for percentile in raw_percentiles.split(","):
        if percentile.isdigit():
            all_percentiles.append(percentile)
        else:
            start, end = percentile.split("-")
            start = int(start)
            end = int(end)
            for i in range(start, end + 1):
                all_percentiles.append(str(i))
    return all_percentiles
