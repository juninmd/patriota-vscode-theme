import json
import os
from playwright.sync_api import sync_playwright

# 1. Read Theme
try:
    with open('themes/patriota-color-theme.json', 'r') as f:
        theme = json.load(f)
except FileNotFoundError:
    print("Error: Theme file not found at themes/patriota-color-theme.json")
    exit(1)

colors = theme.get('colors', {})

# 2. Map Colors to CSS Variables
def get_color(key, default='#000000'):
    return colors.get(key, default)

css_vars = f"""
    --activityBar-bg: {get_color('activityBar.background', '#333')};
    --activityBar-fg: {get_color('activityBar.foreground', '#fff')};
    --activityBar-border: {get_color('activityBar.border', 'transparent')};

    --sideBar-bg: {get_color('sideBar.background', '#252526')};
    --sideBar-fg: {get_color('sideBar.foreground', '#ccc')};
    --sideBar-border: {get_color('sideBar.border', 'transparent')};
    --sideBar-header-fg: {get_color('sideBarSectionHeader.foreground', '#ccc')};

    --editor-bg: {get_color('editor.background', '#1e1e1e')};
    --editor-fg: {get_color('editor.foreground', '#d4d4d4')};

    --statusBar-bg: {get_color('statusBar.background', '#007acc')};
    --statusBar-fg: {get_color('statusBar.foreground', '#fff')};
    --statusBar-border: {get_color('statusBar.border', 'transparent')};

    --tab-active-bg: {get_color('tab.activeBackground', '#1e1e1e')};
    --tab-active-fg: {get_color('tab.activeForeground', '#fff')};
    --tab-inactive-bg: {get_color('tab.inactiveBackground', '#2d2d2d')};
    --tab-inactive-fg: {get_color('tab.inactiveForeground', '#969696')};
    --tab-border: {get_color('tab.activeBorderTop', 'transparent')};

    --line-number-fg: {get_color('editorLineNumber.foreground', '#858585')};
"""

# Extract token colors specifically
token_colors = theme.get('tokenColors', [])
syntax_styles = ""

def find_settings(scope_name):
    for token in token_colors:
        scope = token.get('scope')
        # Handle both string and list scopes
        if isinstance(scope, str):
            if scope == scope_name: return token['settings']
        elif isinstance(scope, list):
            if scope_name in scope: return token['settings']
    return {}

# Helper to generate CSS class
def gen_syntax_css(cls, scope):
    settings = find_settings(scope)
    css = f".{cls} {{ "
    if 'foreground' in settings:
        css += f"color: {settings['foreground']}; "
    if 'fontStyle' in settings:
        if 'bold' in settings['fontStyle']: css += "font-weight: bold; "
        if 'italic' in settings['fontStyle']: css += "font-style: italic; "
    css += "}"
    return css

# Map common scopes used in my snippet
syntax_styles += gen_syntax_css('keyword', 'keyword')
syntax_styles += gen_syntax_css('control', 'keyword.control')
syntax_styles += gen_syntax_css('string', 'string')
syntax_styles += gen_syntax_css('function', 'entity.name.function')
syntax_styles += gen_syntax_css('comment', 'comment')
syntax_styles += gen_syntax_css('number', 'constant.numeric')
syntax_styles += gen_syntax_css('class', 'entity.name.type')

# 3. HTML Template
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<style>
    :root {{
        {css_vars}
        --font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }}
    body {{ margin: 0; padding: 0; display: flex; height: 100vh; font-family: -apple-system, BlinkMacSystemFont, sans-serif; overflow: hidden; background: #000; }}

    .window {{ display: flex; flex-direction: column; height: 100%; width: 100%; }}

    .main-container {{ display: flex; flex: 1; overflow: hidden; }}

    .activity-bar {{ width: 50px; background: var(--activityBar-bg); display: flex; flex-direction: column; align-items: center; padding-top: 10px; border-right: 1px solid var(--activityBar-border); }}
    .icon {{ width: 24px; height: 24px; background: var(--activityBar-fg); opacity: 0.4; margin-bottom: 25px; -webkit-mask-size: cover; }}
    .icon.active {{ opacity: 1; border-left: 2px solid var(--tab-border); }}

    .side-bar {{ width: 200px; background: var(--sideBar-bg); color: var(--sideBar-fg); border-right: 1px solid var(--sideBar-border); display: flex; flex-direction: column; }}
    .side-bar-header {{ padding: 10px 20px; font-size: 11px; text-transform: uppercase; font-weight: bold; display: flex; justify-content: space-between; align-items: center; color: var(--sideBar-header-fg); }}
    .file-tree {{ padding: 0; }}
    .file-item {{ padding: 4px 20px; font-size: 13px; display: flex; align-items: center; cursor: pointer; }}
    .file-item:hover {{ background: #ffffff11; }}
    .file-item.selected {{ background: #ffffff22; color: #fff; }}
    .file-icon {{ width: 14px; height: 14px; margin-right: 6px; display: inline-block; background: #888; }}

    .editor-group {{ flex: 1; display: flex; flex-direction: column; background: var(--editor-bg); }}

    .tabs {{ height: 35px; background: var(--tab-inactive-bg); display: flex; overflow-x: auto; }}
    .tab {{ padding: 0 15px; display: flex; align-items: center; font-size: 13px; color: var(--tab-inactive-fg); border-right: 1px solid #00000022; cursor: pointer; min-width: 100px; }}
    .tab.active {{ background: var(--tab-active-bg); color: var(--tab-active-fg); border-top: 2px solid var(--tab-border); }}

    .editor-container {{ flex: 1; display: flex; font-family: var(--font-family); font-size: 14px; padding-top: 10px; overflow: hidden; }}
    .gutter {{ width: 50px; text-align: right; padding-right: 15px; color: var(--line-number-fg); user-select: none; line-height: 1.5; }}
    .code-area {{ color: var(--editor-fg); white-space: pre; line-height: 1.5; }}

    .status-bar {{ height: 22px; background: var(--statusBar-bg); color: var(--statusBar-fg); border-top: 1px solid var(--statusBar-border); display: flex; align-items: center; padding: 0 10px; font-size: 12px; justify-content: space-between; }}
    .status-item {{ margin-right: 15px; display: flex; align-items: center; }}

    /* Syntax Highlighting */
    {syntax_styles}
</style>
</head>
<body>

<div class="window">
    <div class="main-container">
        <!-- Activity Bar -->
        <div class="activity-bar">
            <div class="icon active" style="background: var(--activityBar-fg);"></div> <!-- Files -->
            <div class="icon" style="background: var(--activityBar-fg);"></div> <!-- Search -->
            <div class="icon" style="background: var(--activityBar-fg);"></div> <!-- Git -->
            <div class="icon" style="background: var(--activityBar-fg);"></div> <!-- Debug -->
        </div>

        <!-- Side Bar -->
        <div class="side-bar">
            <div class="side-bar-header">Explorer</div>
            <div class="file-tree">
                <div class="side-bar-header" style="padding-left: 10px;">PATRIOTA-THEME</div>
                <div class="file-item selected"><span class="file-icon" style="background: #e37933;"></span>main.py</div>
                <div class="file-item"><span class="file-icon" style="background: #cbcb41;"></span>utils.js</div>
                <div class="file-item"><span class="file-icon" style="background: #4d78cc;"></span>styles.css</div>
                <div class="file-item"><span class="file-icon" style="background: #ccc;"></span>README.md</div>
            </div>
        </div>

        <!-- Editor Area -->
        <div class="editor-group">
            <div class="tabs">
                <div class="tab active">main.py</div>
                <div class="tab">utils.js</div>
                <div class="tab">styles.css</div>
            </div>

            <div class="editor-container">
                <div class="gutter">
                    1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11
                </div>
                <div class="code-area">
<span class="keyword">import</span> <span class="class">math</span>

<span class="comment"># Verifica se um número é patriota (exemplo)</span>
<span class="keyword">def</span> <span class="function">verificar_brasilidade</span>(<span class="class">valor</span>):
    <span class="control">if</span> <span class="class">valor</span> >= <span class="number">100</span>:
        <span class="control">return</span> <span class="keyword">True</span>

    <span class="keyword">print</span>(<span class="string">f"Analisando o valor: {{valor}}"</span>)

    <span class="class">resultado</span> = <span class="class">math</span>.<span class="function">sqrt</span>(<span class="class">valor</span>)
    <span class="control">return</span> <span class="class">resultado</span> > <span class="number">10</span>

<span class="comment">/*
   Este é um comentário longo
   para demonstrar o itálico
*/</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Status Bar -->
    <div class="status-bar">
        <div class="status-item"><span style="margin-right:5px">master*</span></div>
        <div class="status-item">
            <span style="margin-right: 15px;">Ln 11, Col 1</span>
            <span style="margin-right: 15px;">UTF-8</span>
            <span>Python</span>
        </div>
    </div>
</div>

</body>
</html>
"""

# Write HTML file
preview_path = 'preview.html'
with open(preview_path, 'w') as f:
    f.write(html_content)

print(f"Generated HTML preview at {preview_path}")

# Run Playwright to Screenshot
try:
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set viewport to standard extension screenshot size
        page.set_viewport_size({"width": 1024, "height": 768})

        url = f"file://{os.path.abspath(preview_path)}"
        print(f"Navigating to {url}...")
        page.goto(url)

        output_image = "theme_preview.png"
        page.screenshot(path=output_image)
        print(f"Screenshot saved to {output_image}")

        browser.close()
except Exception as e:
    print(f"Error generating screenshot: {e}")
    # We don't exit with error because the HTML was generated successfully,
    # and maybe the user doesn't have browsers installed in their env if they run it locally.
