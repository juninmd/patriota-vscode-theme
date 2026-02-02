import pytest
from scripts.validate_theme import validate_hex

@pytest.mark.parametrize("color,expected", [
    ("#ffffff", True),
    ("#000000", True),
    ("#123456", True),
    ("#ABCDEF", True),
    ("#abcdef", True),
    ("#12345678", True), # 8 digits (Alpha)
    ("#fff", True),      # 3 digits
    ("#000", True),
    ("#abcd", True),     # 4 digits (Alpha)
    ("ffffff", False),   # Missing #
    ("#12345", False),   # 5 digits (Invalid)
    ("#1234567", False), # 7 digits (Invalid)
    ("#GGGGGG", False),  # Invalid chars
    ("", False),         # Empty
    ("#", False),        # Just #
])
def test_validate_hex(color, expected):
    assert validate_hex(color, "test_key") == expected
