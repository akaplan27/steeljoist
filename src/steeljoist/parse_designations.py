import re

def parse_sji_joist_designation(designation):
    """
    Parse a standard SJI joist designation.

    Examples:
        "24K5"    -> ("24", "K", "5")
        "30LH06"  -> ("30", "LH", "06")
        "40DLH12" -> ("40", "DLH", "12")

    Returns:
        tuple: (depth, series, designation_number)

    Raises:
        ValueError: If the designation is not valid.
    """

    pattern = r"^(\d+)(K|LH|DLH)(\d+)$"

    match = re.match(pattern, designation.upper())

    if not match:
        raise ValueError(f"Invalid SJI joist designation: {designation}")

    depth, series, number = match.groups()

    return depth, series, number


if __name__ == "__main__":
    # Example usage
    print(parse_sji_joist_designation("24K5"))
    # Output: ('24', 'K', '5')

    print(parse_sji_joist_designation("30LH06"))
    # Output: ('30', 'LH', '06')