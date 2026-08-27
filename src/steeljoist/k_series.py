
K_SERIES_DEPTHS = {
    1: (10, 12, 14),
    2: (16,),
    3: (12, 14, 16, 18, 20),
    4: (14, 16, 18, 20, 22, 24),
    5: (12, 16, 18, 20, 22, 24, 26),
    6: (14, 16, 18, 20, 22, 24, 26, 28),
    7: (16, 18, 20, 22, 24, 26, 28, 30),
    8: (24, 26, 28, 30),
    9: (16, 18, 20, 22, 24, 26, 28, 30),
    10: (18, 20, 22, 24, 26, 28, 30),
    11: (22, 30),
    12: (24, 26, 28, 30),
}

K_SERIES_DESIGNATIONS = tuple(
    f"{depth}K{section_number}"
    for section_number, depths in K_SERIES_DEPTHS.items()
    for depth in depths
)

K_SERIES_DESIGNATION_SET = frozenset(K_SERIES_DESIGNATIONS)

def is_standard_k_series_designation(designation: str) -> bool:
    """Return whether a designation is a standard K-Series joist."""
    return designation.upper() in K_SERIES_DESIGNATION_SET