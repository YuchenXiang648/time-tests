import times
import datetime
import pytest
import yaml
from pathlib import Path

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


def _load_overlap_params_from_yaml():
    """Read overlap cases from fixture.yaml and build parametrization tuples."""
    data = yaml.safe_load(Path("fixture.yaml").read_text())
    params = []
    for name, case in data["cases"].items():
        r1 = case["range1"]
        r2 = case["range2"]
        tr1 = times.time_range(
            r1["start"], r1["end"], r1.get("n", 1), r1.get("gap", 0)
        )
        tr2 = times.time_range(
            r2["start"], r2["end"], r2.get("n", 1), r2.get("gap", 0)
        )
        expected = [tuple(x) for x in case.get("expected", [])]
        params.append((tr1, tr2, expected))
    return params


@pytest.mark.parametrize(
    "time_range_1, time_range_2, expected", _load_overlap_params_from_yaml()
)
def test_compute_overlap_from_yaml(time_range_1, time_range_2, expected):
    got = times.compute_overlap_time(time_range_1, time_range_2)
    assert got == expected