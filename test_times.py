import times
import datetime
import pytest


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


def mk(start, end, n=1, gap=0):
    return times.time_range(start, end, n, gap)

@pytest.mark.parametrize(
    "time_range_1, time_range_2, expected",
    [
        (
            mk("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            mk("2010-01-12 10:30:00", "2010-01-12 11:30:00"),
            [("2010-01-12 10:30:00", "2010-01-12 11:30:00")],
        ),

        (
            mk("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            mk("2010-01-12 11:00:00", "2010-01-12 12:00:00"),
            [],
        ),

        (
            mk("2010-01-12 10:00:00", "2010-01-12 11:00:00", 2),
            mk("2010-01-12 10:30:00", "2010-01-12 11:30:00", 2),
            [("2010-01-12 10:30:00", "2010-01-12 11:00:00")],
        ),

        (
            mk("2010-01-12 09:00:00", "2010-01-12 10:00:00"),
            mk("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            [],
        ),
    ],
)
def test_compute_overlap_parametrized(time_range_1, time_range_2, expected):
    got = times.compute_overlap_time(time_range_1, time_range_2)
    assert got == expected