from bisect import bisect_left
from math import inf

from steeljoist import parse_sji_joist_designation


# Limiting spans for the required number of rows of horizontal bridging.
#
# Data are based on SJI 100-2025, Table 5.5-1. Valid K-Series depth and
# section-number combinations are based on the standard designations in
# the SJI Load Tables.
#
# Each tuple contains the maximum span, in feet, corresponding to each
# number of required bridging rows. For example:
#
#     (20, 30, 42, 48)
#
# represents:
#
#     span <= 20 ft        -> 1 row
#     20 ft < span <= 30   -> 2 rows
#     30 ft < span <= 42   -> 3 rows
#     42 ft < span <= 48   -> 4 rows
#
# K-Series data are keyed by (section_number, depth_in).

K_SERIES_BRIDGING_LIMITS = {
    # K1
    (1, 10): (17, 26, 28),
    (1, 12): (17, 26, 28),
    (1, 14): (17, 26, 28),

    # K2
    (2, 16): (21, 30, 32),

    # K3
    (3, 12): (18, 26, 40),
    (3, 14): (18, 26, 40),
    (3, 16): (18, 26, 40),
    (3, 18): (18, 26, 40),
    (3, 20): (18, 26, 40),

    # K4
    (4, 14): (20, 30, 41, 48),
    (4, 16): (20, 30, 41, 48),
    (4, 18): (20, 30, 41, 48),
    (4, 20): (20, 30, 41, 48),
    (4, 22): (20, 30, 41, 48),
    (4, 24): (20, 30, 41, 48),

    # K5
    (5, 12): (20, 30, 42, 48),
    (5, 16): (20, 30, 42, 48),
    (5, 18): (20, 30, 42, 48),
    (5, 20): (20, 30, 42, 48),
    (5, 22): (20, 30, 42, 48),
    (5, 24): (20, 30, 42, 48),
    (5, 26): (28, 41, 52),

    # K6
    (6, 14): (20, 31, 42, 48),
    (6, 16): (20, 31, 42, 48),
    (6, 18): (20, 31, 42, 48),
    (6, 20): (20, 31, 42, 48),
    (6, 22): (20, 31, 42, 48),
    (6, 24): (20, 31, 42, 48),
    (6, 26): (28, 41, 54, 56),
    (6, 28): (28, 41, 54, 56),

    # K7
    (7, 16): (23, 34, 48),
    (7, 18): (23, 34, 48),
    (7, 20): (23, 34, 48),
    (7, 22): (23, 34, 48),
    (7, 24): (23, 34, 48),
    (7, 26): (29, 44, 60),
    (7, 28): (29, 44, 60),
    (7, 30): (29, 44, 60),

    # K8
    (8, 24): (25, 39, 48),
    (8, 26): (29, 44, 60),
    (8, 28): (29, 44, 60),
    (8, 30): (29, 44, 60),

    # K9
    (9, 16): (22, 34, 48),
    (9, 18): (22, 34, 48),
    (9, 20): (22, 34, 48),
    (9, 22): (22, 34, 48),
    (9, 24): (22, 34, 48),
    (9, 26): (29, 44, 60),
    (9, 28): (29, 44, 60),
    (9, 30): (29, 44, 60),

    # K10
    (10, 18): (22, 38, 48),
    (10, 20): (22, 38, 48),
    (10, 22): (22, 38, 48),
    (10, 24): (22, 38, 48),
    (10, 26): (29, 48, 60),
    (10, 28): (29, 48, 60),
    (10, 30): (29, 48, 60),

    # K11
    (11, 22): (24, 39, 44),
    (11, 30): (34, 49, 60),

    # K12
    (12, 24): (25, 43, 48),
    (12, 26): (29, 47, 60),
    (12, 28): (29, 47, 60),
    (12, 30): (29, 47, 60),
}


# LH- and DLH-Series limits depend only on section number.
#
# `inf` represents the final "or greater" range in SJI Table 5.5-1.
# Therefore, unlike the K-Series data, these entries have no finite
# maximum span.

LH_DLH_SERIES_BRIDGING_LIMITS = {
    2: (20, 30, 40, inf),
    3: (20, 30, 40, inf),
    4: (22, 33, 44, 55, inf),
    5: (22, 33, 44, 55, inf),
    6: (26, 45, 60, 75, inf),
    7: (26, 45, 60, 75, inf),
    8: (26, 45, 60, 75, inf),
    9: (26, 48, 64, 80, inf),
    10: (28, 54, 72, 90, inf),
    11: (30, 54, 72, 90, 108, inf),
    12: (34, 55, 74, 92, 111, inf),
    13: (36, 63, 84, 105, 126, inf),
    14: (38, 64, 86, 107, 129, inf),
    15: (42, 73, 98, 122, 147, inf),
    16: (44, 75, 100, 125, 150, 175, inf),
    17: (44, 75, 100, 125, 150, 175, inf),
    18: (52, 78, 104, 130, 156, 182, 208, 234, inf),
    19: (52, 78, 104, 130, 156, 182, 208, 234, inf),
    20: (52, 78, 104, 130, 156, 182, 208, 234, inf),
    21: (60, 90, 120, 150, 180, 210, inf),
    22: (60, 90, 120, 150, 180, 210, inf),
    23: (60, 90, 120, 150, 180, 210, inf),
    24: (60, 90, 120, 150, 180, 210, inf),
    25: (60, 90, 120, 150, 180, 210, inf),
}


def required_bridging_rows(designation: str, span_ft: float) -> int:
    """Return the required number of rows of horizontal bridging.

    The required number of bridging rows is determined from the limiting
    spans in SJI 100-2025, Table 5.5-1.

    Parameters
    ----------
    designation : str
        Standard SJI joist designation, such as ``"24K5"``,
        ``"32LH6"``, or ``"80DLH15"``.
    span_ft : float
        Joist span in feet.

    Returns
    -------
    int
        Number of required rows of horizontal bridging.

    Raises
    ------
    ValueError
        If ``span_ft`` is not positive.
    ValueError
        If the joist series is not K, LH, or DLH.
    ValueError
        If a K-Series depth and section-number combination is not a
        standard designation represented in the SJI Load Tables.
    ValueError
        If an LH- or DLH-Series section number is not represented in
        SJI Table 5.5-1.
    ValueError
        If the span exceeds the maximum limiting span for a K-Series
        joist.

    Notes
    -----
    The limiting-span tuples contain the maximum span for each required
    number of bridging rows. ``bisect_left`` is used so that a span
    exactly equal to a limiting span remains in the lower row-count
    category.

    For example, limiting spans of ``(20, 30, 42, 48)`` give:

    * 1 row for spans up to and including 20 ft
    * 2 rows for spans greater than 20 ft through 30 ft
    * 3 rows for spans greater than 30 ft through 42 ft
    * 4 rows for spans greater than 42 ft through 48 ft

    LH- and DLH-Series entries end with ``inf`` because the final range
    in SJI Table 5.5-1 extends to greater spans.

    References
    ----------
    Steel Joist Institute, SJI 100-2025, Table 5.5-1.
    Steel Joist Institute Load Tables for standard K-Series designations.
    """
    if span_ft <= 0:
        raise ValueError(
            f"Span must be greater than zero; received {span_ft} ft."
        )

    depth, series, section_number = parse_sji_joist_designation(designation)

    if series == "K":
        key = (section_number, depth)

        try:
            limiting_spans = K_SERIES_BRIDGING_LIMITS[key]
        except KeyError:
            raise ValueError(
                f"{designation} is not a standard K-Series designation "
                "represented in the SJI Load Tables."
            ) from None

    elif series in ("LH", "DLH"):
        try:
            limiting_spans = LH_DLH_SERIES_BRIDGING_LIMITS[section_number]
        except KeyError:
            raise ValueError(
                f"Unknown section number for {series}-Series joist: "
                f"{section_number}"
            ) from None

    else:
        raise ValueError(f"Unknown joist series: {series}")

    if span_ft > limiting_spans[-1]:
        raise ValueError(
            f"Span ({span_ft} ft) exceeds the maximum tabulated span "
            f"for {designation} ({limiting_spans[-1]} ft)."
        )

    return bisect_left(limiting_spans, span_ft) + 1