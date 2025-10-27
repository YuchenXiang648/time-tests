import datetime as dt
import times


def _fmt(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%d %H:%M:%S")


def test_time_range_basic():
    result = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2)
    expected = [
        ("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
        ("2010-01-12 11:00:00", "2010-01-12 12:00:00"),
    ]
    assert result == expected


def test_time_range_with_gap():
    start = dt.datetime(2010, 1, 12, 10, 0, 0)
    end = dt.datetime(2010, 1, 12, 10, 30, 0)
    gap = 60

    result = times.time_range(_fmt(start), _fmt(end), 2, gap)

    seg = dt.timedelta(seconds=(end - start).seconds - gap) / 2 
    s1 = start
    e1 = s1 + seg
    s2 = e1 + dt.timedelta(seconds=gap)
    e2 = s2 + seg
    expected = [(_fmt(s1), _fmt(e1)), (_fmt(s2), _fmt(e2))]

    assert result == expected

def test_no_overlap_ranges():
    r1 = times.time_range("2010-01-12 10:00:00", "2010-01-12 10:10:00")
    r2 = times.time_range("2010-01-12 10:10:00", "2010-01-12 10:20:00")
    overlap = times.compute_overlap_time(r1, r2)
    assert overlap == [("2010-01-12 10:10:00", "2010-01-12 10:10:00")]


<<<<<<< HEAD
    assert isinstance(overlap, list)
    assert all(len(x) == 2 for x in overlap)
    assert overlap[0][0] >= "2010-01-12 10:30:00"


def test_no_overlap():
    """Two time ranges that do not overlap."""
    range1 = times.time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    range2 = times.time_range("2010-01-12 11:00:00", "2010-01-12 12:00:00")
    overlap = times.compute_overlap_time(range1, range2)
    for start, end in overlap:
        assert start == end, f"Expected no overlap, but got {start} to {end}"


def test_multiple_intervals_overlap():
    """Two ranges that both contain several intervals each."""
    range1 = times.time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00", 2)
    range2 = times.time_range("2010-01-12 10:30:00", "2010-01-12 11:30:00", 2)
    overlap = times.compute_overlap_time(range1, range2)
    for start, end in overlap:
        assert start <= end, "Overlap start is after end"
    assert any(start != end for start, end in overlap), "Expected at least one non-zero overlap"


def test_end_equals_start():
    """Two time ranges that end exactly when the other starts."""
    range1 = times.time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00")
    range2 = times.time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    overlap = times.compute_overlap_time(range1, range2)

    for start, end in overlap:
        assert start == end, f"Expected exact boundary overlap, but got {start} to {end}"
=======
def test_both_have_several_intervals():
    r1 = times.time_range("2010-01-12 10:00:00", "2010-01-12 10:20:00", 2, 60)
    r2 = times.time_range("2010-01-12 10:05:00", "2010-01-12 10:25:00", 2, 60)
    overlap = times.compute_overlap_time(r1, r2)
    expected = [
        ("2010-01-12 10:05:00", "2010-01-12 10:09:30"),
        ("2010-01-12 10:10:30", "2010-01-12 10:14:30"),
        ("2010-01-12 10:15:30", "2010-01-12 10:20:00"),
    ]
    assert overlap == expected



def test_touching_endpoints_are_not_overlap():
    r1 = times.time_range("2010-01-12 10:00:00", "2010-01-12 10:30:00")
    r2 = times.time_range("2010-01-12 10:30:00", "2010-01-12 11:00:00")
    overlap = times.compute_overlap_time(r1, r2)
    assert overlap == [("2010-01-12 10:30:00", "2010-01-12 10:30:00")]
>>>>>>> 6f9c7f2 (add tests and update compute_overlap_time (Answers UCL-COMP0233-25-26/RSE-Classwork#15))
