import datetime


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    from datetime import datetime
    fmt = "%Y-%m-%d %H:%M:%S"
    overlap_time = []

    for start1, end1 in range1:
        for start2, end2 in range2:
            s1 = datetime.strptime(start1, fmt)
            e1 = datetime.strptime(end1, fmt)
            s2 = datetime.strptime(start2, fmt)
            e2 = datetime.strptime(end2, fmt)
            low = max(s1, s2)
            high = min(e1, e2)
            if low < high:
                overlap_time.append((low.strftime(fmt), high.strftime(fmt)))
    return overlap_time

if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))