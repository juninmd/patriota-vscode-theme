import json

import pytest

from scripts.validate_theme import calculate_contrast_ratio

THEMES = ["themes/patriota-color-theme.json", "themes/patriota-light-color-theme.json"]
# Selected/focused rows in Explorer, Quick Open and lists: text must stay readable (WCAG AA).
PAIRS = [
    ("list.activeSelectionForeground", "list.activeSelectionBackground"),
    ("list.focusForeground", "list.focusBackground"),
    # Matched characters in a selected row: VS Code uses focusHighlightForeground when set.
    ("list.focusHighlightForeground|list.highlightForeground", "list.activeSelectionBackground"),
    ("quickInputList.focusForeground", "quickInputList.focusBackground"),
]


@pytest.mark.parametrize("path", THEMES)
@pytest.mark.parametrize("fg_key,bg_key", PAIRS)
def test_selected_list_rows_are_readable(path, fg_key, bg_key):
    with open(path, encoding="utf-8") as f:
        colors = json.load(f)["colors"]
    fg_key = next((k for k in fg_key.split("|") if k in colors), fg_key)
    if fg_key not in colors or bg_key not in colors:
        pytest.skip(f"{fg_key} or {bg_key} not set")
    ratio = calculate_contrast_ratio(colors[fg_key], colors[bg_key])
    assert ratio >= 4.5, f"{fg_key} {colors[fg_key]} on {bg_key} {colors[bg_key]}: {ratio:.2f}:1"
