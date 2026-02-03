import json
import re
import sys
import os

def validate_hex(color, key):
    """
    Validates that a color string is in a valid Hex format.
    """
    if not isinstance(color, str):
        print(f"ERROR: Color value for key '{key}' must be a string, but got {type(color).__name__}.", file=sys.stderr)
        return False
    # Regex for #RGB, #RGBA, #RRGGBB, or #RRGGBBAA
    if not re.match(r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$', color):
        print(f"ERROR: Invalid color format '{color}' for key '{key}'. Expected #RGB, #RGBA, #RRGGBB, or #RRGGBBAA.", file=sys.stderr)
        return False
    return True

def hex_to_rgb(hex_color):
    """Converts a hex color string to an (r, g, b, a) tuple."""
    hex_color = hex_color.lstrip('#')
    length = len(hex_color)

    if length == 3: # RGB
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = 255
    elif length == 4: # RGBA
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = int(hex_color[3] * 2, 16)
    elif length == 6: # RRGGBB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = 255
    elif length == 8: # RRGGBBAA
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16)
    else:
        return None

    return (r, g, b, a)

def get_relative_luminance(rgb):
    """Calculates relative luminance from RGB components (0-255)."""
    # Formula from WCAG 2.0
    components = []
    for c in rgb[:3]:
        c = c / 255.0
        if c <= 0.03928:
            components.append(c / 12.92)
        else:
            components.append(((c + 0.055) / 1.055) ** 2.4)

    r, g, b = components
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def calculate_contrast_ratio(color1, color2):
    """
    Calculates contrast ratio between two hex colors.
    Returns None if colors are invalid or too transparent to judge easily.
    """
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)

    if not c1 or not c2:
        return None

    # Skip validation if alpha is significant (arbitrary threshold < 255 for strict, or lower)
    # Let's skip if < 200 (~80%) to avoid false positives on transparent overlays
    if c1[3] < 200 or c2[3] < 200:
        return None

    l1 = get_relative_luminance(c1)
    l2 = get_relative_luminance(c2)

    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def validate_theme(filepath):
    """
    Validates the theme JSON structure, color formats, and accessibility contrast.
    """
    print(f"Validating {filepath}...")
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return False

    try:
        with open(filepath, 'r') as f:
            theme = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        return False

    success = True
    warnings = []

    colors = theme.get('colors', {})
    editor_bg = colors.get('editor.background')

    # Validate 'colors'
    if not isinstance(colors, dict):
        print("ERROR: 'colors' field must be a dictionary.")
        success = False
    else:
        for key, value in colors.items():
            if not validate_hex(value, f"colors.{key}"):
                success = False

    # Check editor foreground contrast if background exists
    if editor_bg and validate_hex(editor_bg, 'editor.background'):
        editor_fg = colors.get('editor.foreground')
        if editor_fg and validate_hex(editor_fg, 'editor.foreground'):
            ratio = calculate_contrast_ratio(editor_fg, editor_bg)
            if ratio and ratio < 4.5:
                warnings.append(f"Low contrast for 'editor.foreground': {ratio:.2f}:1 (Expected >= 4.5:1)")

    # Validate 'tokenColors'
    token_colors = theme.get('tokenColors', [])
    if not isinstance(token_colors, list):
        print("ERROR: 'tokenColors' field must be a list.")
        success = False
    else:
        for i, token in enumerate(token_colors):
            settings = token.get('settings', {})
            name = token.get('name', f"Token[{i}]")

            fg = settings.get('foreground')
            if fg:
                if not validate_hex(fg, f"tokenColors[{i}].settings.foreground"):
                    success = False
                elif editor_bg:
                    # Check contrast against editor background
                    ratio = calculate_contrast_ratio(fg, editor_bg)
                    if ratio and ratio < 4.5:
                        warnings.append(f"Low contrast for token '{name}': {ratio:.2f}:1 (Expected >= 4.5:1)")

            bg = settings.get('background')
            if bg:
                if not validate_hex(bg, f"tokenColors[{i}].settings.background"):
                    success = False

    if warnings:
        print("\n⚠️  Accessibility Warnings:")
        for w in warnings:
            print(f"  - {w}")
        print("")

    if success:
        print("✅ Theme validation passed!")
        return True
    else:
        print("❌ Theme validation failed.")
        return False

if __name__ == "__main__":
    theme_path = os.path.join('themes', 'patriota-color-theme.json')
    if not validate_theme(theme_path):
        sys.exit(1)
