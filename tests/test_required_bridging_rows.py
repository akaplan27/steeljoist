import pytest

from steeljoist import required_bridging_rows


# Representative valid cases
@pytest.mark.parametrize(
    ("designation", "span_ft", "expected_rows"),
    [
        # K-Series
        ("10K1", 10, 1),
        ("10K1", 17, 1),
        ("10K1", 18, 2),
        ("10K1", 26, 2),
        ("10K1", 27, 3),
        ("10K1", 28, 3),

        ("24K5", 20, 1),
        ("24K5", 21, 2),
        ("24K5", 30, 2),
        ("24K5", 31, 3),
        ("24K5", 42, 3),
        ("24K5", 43, 4),
        ("24K5", 48, 4),

        ("26K5", 28, 1),
        ("26K5", 29, 2),
        ("26K5", 41, 2),
        ("26K5", 42, 3),
        ("26K5", 52, 3),

        ("30K12", 29, 1),
        ("30K12", 30, 2),
        ("30K12", 47, 2),
        ("30K12", 48, 3),
        ("30K12", 60, 3),

        # LH-Series
        ("32LH6", 26, 1),
        ("32LH6", 27, 2),
        ("32LH6", 45, 2),
        ("32LH6", 46, 3),
        ("32LH6", 60, 3),
        ("32LH6", 61, 4),

        # DLH-Series
        ("80DLH15", 42, 1),
        ("80DLH15", 43, 2),
        ("80DLH15", 73, 2),
        ("80DLH15", 74, 3),
        ("80DLH15", 98, 3),
        ("80DLH15", 99, 4),
        ("80DLH15", 122, 4),
        ("80DLH15", 123, 5),
        ("80DLH15", 147, 5),
        ("80DLH15", 148, 6),
    ],
)
def test_required_bridging_rows(designation, span_ft, expected_rows):
    assert required_bridging_rows(designation, span_ft) == expected_rows


# Exceeded K-Series spans
@pytest.mark.parametrize(
    ("designation", "span_ft"),
    [
        ("10K1", 29),
        ("24K5", 49),
        ("26K5", 53),
        ("28K6", 57),
        ("30K12", 61),
    ],
)
def test_span_exceeding_k_series_limit_raises(designation, span_ft):
    with pytest.raises(ValueError, match="exceeds"):
        required_bridging_rows(designation, span_ft)


# Invalid K-Series designations
@pytest.mark.parametrize(
    "designation",
    [
        "16K1",   # K1 only permits depths 10, 12, and 14
        "14K2",   # K2 only permits depth 16
        "14K5",   # not listed for K5
        "22K8",   # K8 starts at depth 24
        "24K11",  # K11 only permits 22 and 30
        "28K11",
    ],
)
def test_nonstandard_k_designation_raises(designation):
    with pytest.raises(ValueError):
        required_bridging_rows(designation, 20)


# Invalid span input
@pytest.mark.parametrize("span_ft", [0, -1, -20.5])
def test_nonpositive_span_raises(span_ft):
    with pytest.raises(ValueError, match="greater than zero"):
        required_bridging_rows("24K5", span_ft)


# LH/DLH open-ended final ranges
def test_lh_dlh_final_range_has_no_upper_limit():
    assert required_bridging_rows("32LH06", 1000) == 5
    assert required_bridging_rows("80DLH15", 1000) == 6
