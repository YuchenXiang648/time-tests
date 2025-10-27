import times
import datetime


def test_time_range_basic():
    """Test that time_range splits interval correctly."""
    result = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2)
    expected = [
        ("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
        ("2010-01-12 11:00:00", "2010-01-12 12:00:00")
    ]
    assert result == expected


def test_time_range_with_gap():
    """Test that gap_between_intervals_s adds correct spacing."""
    result = times.time_range("2010-01-12 10:00:00", "2010-01-12 10:30:00", 2, 60)
    expected_start_1 = datetime.datetime(2010, 1, 12, 10, 0, 0)
    expected_end_1 = expected_start_1 + datetime.timedelta(seconds=870)
    expected_start_2 = expected_end_1 + datetime.timedelta(seconds=60)
    expected_end_2 = expected_start_2 + datetime.timedelta(seconds=870)
    expected = [
        (expected_start_1.strftime("%Y-%m-%d %H:%M:%S"), expected_end_1.strftime("%Y-%m-%d %H:%M:%S")),
        (expected_start_2.strftime("%Y-%m-%d %H:%M:%S"), expected_end_2.strftime("%Y-%m-%d %H:%M:%S"))
    ]
    assert result == expected


def test_compute_overlap_time():
    """Test overlap between two simple ranges."""
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    overlap = times.compute_overlap_time(large, short)

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
