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


import pytest
import times

def test_time_range_backwards_raises():
    with pytest.raises(ValueError, match="end_time is before start_time"):
        times.time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
