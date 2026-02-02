import json
import re
import sys
import os

def validate_hex(color, key):
    # Regex for #RGB, #RGBA, #RRGGBB, or #RRGGBBAA
    if not re.match(r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$', color):
        print(f"ERROR: Invalid color format '{color}' for key '{key}'. Expected #RGB, #RGBA, #RRGGBB, or #RRGGBBAA.")
        return False
    return True

def validate_theme(filepath):
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

    # Validate 'colors'
    colors = theme.get('colors', {})
    if not isinstance(colors, dict):
        print("ERROR: 'colors' field must be a dictionary.")
        success = False
    else:
        for key, value in colors.items():
            if not validate_hex(value, f"colors.{key}"):
                success = False

    # Validate 'tokenColors'
    token_colors = theme.get('tokenColors', [])
    if not isinstance(token_colors, list):
        print("ERROR: 'tokenColors' field must be a list.")
        success = False
    else:
        for i, token in enumerate(token_colors):
            settings = token.get('settings', {})
            if 'foreground' in settings:
                if not validate_hex(settings['foreground'], f"tokenColors[{i}].settings.foreground"):
                    success = False
            # background is less common in tokenColors but possible
            if 'background' in settings:
                 if not validate_hex(settings['background'], f"tokenColors[{i}].settings.background"):
                    success = False

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
