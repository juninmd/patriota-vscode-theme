import pytest
from scripts.validate_theme import hex_to_rgb, get_relative_luminance, calculate_contrast_ratio

class TestContrastValidation:

    @pytest.mark.parametrize("hex_code,expected", [
        ("#ffffff", (255, 255, 255, 255)),
        ("#000000", (0, 0, 0, 255)),
        ("#ff0000", (255, 0, 0, 255)),
        ("#00ff00", (0, 255, 0, 255)),
        ("#0000ff", (0, 0, 255, 255)),
        ("#fff", (255, 255, 255, 255)),
        ("#f00", (255, 0, 0, 255)),
        ("#ffffff80", (255, 255, 255, 128)),
    ])
    def test_hex_to_rgb(self, hex_code, expected):
        assert hex_to_rgb(hex_code) == expected

    def test_hex_to_rgb_short_alpha(self):
        # Separate test for short hex with alpha because calculation might vary slightly
        # depending on implementation (0x8 vs 0x88)
        # My implementation does: hex_color[3] * 2, so '8' becomes '88' => 136
        res = hex_to_rgb("#fff8")
        assert res == (255, 255, 255, 136)

    def test_get_relative_luminance(self):
        # Black
        assert get_relative_luminance((0, 0, 0, 255)) == 0
        # White
        assert get_relative_luminance((255, 255, 255, 255)) == 1
        # Red (standard relative luminance is ~0.2126)
        lum_red = get_relative_luminance((255, 0, 0, 255))
        assert 0.21 < lum_red < 0.22

    def test_calculate_contrast_ratio(self):
        white = "#ffffff"
        black = "#000000"

        # Contrast of black and white should be 21:1
        ratio = calculate_contrast_ratio(white, black)
        assert ratio == 21.0

        # Same color should be 1:1
        assert calculate_contrast_ratio(white, white) == 1.0

        # Check ordering doesn't matter
        assert calculate_contrast_ratio(black, white) == 21.0

    def test_contrast_ratio_alpha_handling(self):
        # Very transparent colors should return None
        transparent = "#ffffff00"
        opaque = "#000000"

        assert calculate_contrast_ratio(transparent, opaque) is None
        assert calculate_contrast_ratio(opaque, transparent) is None
