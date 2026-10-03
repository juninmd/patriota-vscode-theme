"""Gera themes/patriota-light-color-theme.json (variante clara)."""
import json
import os

AZUL, VERDE, VERDE_ESC = "#002776", "#009c3b", "#006b28"
OURO, BRANCO, FUNDO = "#8a6d00", "#ffffff", "#f6faf7"
SIDE, TEXTO, MUDO = "#e6eeff", "#0b1c3d", "#4a5a7d"

COLORS = {
    "editor.background": BRANCO, "editor.foreground": TEXTO,
    "editorLineNumber.foreground": "#0b1c3d77", "editorLineNumber.activeForeground": AZUL,
    "editorCursor.foreground": AZUL, "editor.selectionBackground": "#ffdf0088",
    "editor.lineHighlightBackground": "#ffdf0033", "editor.lineHighlightBorder": "#00000000",
    "editor.findMatchBackground": "#ffdf00cc", "editor.findMatchHighlightBackground": "#ffdf0066",
    "editor.wordHighlightBackground": "#009c3b22", "editorBracketMatch.background": "#009c3b33",
    "editorBracketMatch.border": VERDE,
    "editorBracketHighlight.foreground1": VERDE_ESC, "editorBracketHighlight.foreground2": OURO,
    "editorBracketHighlight.foreground3": AZUL, "editorBracketHighlight.foreground4": "#7a3ea8",
    "editorBracketHighlight.foreground5": "#b34700", "editorBracketHighlight.foreground6": "#005f99",
    "editorIndentGuide.background1": "#0b1c3d1a", "editorIndentGuide.activeBackground1": VERDE,
    "editorGutter.background": BRANCO, "editorGutter.addedBackground": VERDE,
    "editorGutter.modifiedBackground": "#e6b800", "editorGutter.deletedBackground": "#d32f2f",
    "editorError.foreground": "#d32f2f", "editorWarning.foreground": "#b36b00",
    "editorGhostText.foreground": "#0b1c3d66", "editorWidget.background": BRANCO,
    "editorWidget.border": "#002776aa", "editorSuggestWidget.selectedBackground": "#ffdf0066",
    "editorSuggestWidget.highlightForeground": VERDE_ESC, "editorHoverWidget.border": AZUL,
    "activityBar.background": AZUL, "activityBar.foreground": BRANCO,
    "activityBar.inactiveForeground": "#ffffffaa", "activityBar.activeBorder": "#ffdf00",
    "activityBarBadge.background": "#ffdf00", "activityBarBadge.foreground": AZUL,
    "sideBar.background": SIDE, "sideBar.foreground": TEXTO, "sideBar.border": "#00277622",
    "sideBarTitle.foreground": AZUL, "sideBarSectionHeader.background": "#cfe0ff",
    "sideBarSectionHeader.foreground": AZUL,
    "titleBar.activeBackground": AZUL, "titleBar.activeForeground": "#ffdf00",
    "titleBar.inactiveBackground": "#1a3a8f", "titleBar.inactiveForeground": "#ffffffaa",
    "statusBar.background": "#007a2e", "statusBar.foreground": BRANCO,
    "statusBar.debuggingBackground": "#ffdf00", "statusBar.debuggingForeground": AZUL,
    "statusBar.noFolderBackground": AZUL, "statusBarItem.hoverBackground": "#ffffff33",
    "tab.activeBackground": BRANCO, "tab.activeForeground": AZUL, "tab.activeBorderTop": VERDE,
    "tab.inactiveBackground": "#dbe6fb", "tab.inactiveForeground": MUDO, "tab.border": "#00277618",
    "editorGroupHeader.tabsBackground": "#dbe6fb", "breadcrumb.foreground": MUDO,
    "breadcrumb.focusForeground": AZUL, "panel.background": FUNDO, "panel.border": "#00277633",
    "panelTitle.activeForeground": AZUL, "panelTitle.activeBorder": VERDE,
    "panelTitle.inactiveForeground": MUDO,
    "list.activeSelectionBackground": "#007a2e", "list.activeSelectionForeground": BRANCO,
    "list.inactiveSelectionBackground": "#009c3b33", "list.hoverBackground": "#ffdf0055",
    "list.highlightForeground": VERDE_ESC, "list.focusBackground": "#007a2e",
    "list.focusForeground": BRANCO,
    "input.background": BRANCO, "input.border": "#00277655", "input.foreground": TEXTO,
    "focusBorder": VERDE, "button.background": "#007a2e", "button.foreground": BRANCO,
    "button.hoverBackground": VERDE_ESC, "badge.background": AZUL, "badge.foreground": BRANCO,
    "progressBar.background": VERDE, "textLink.foreground": "#0050c8",
    "menu.background": BRANCO, "menu.foreground": TEXTO, "menu.selectionBackground": "#ffdf00aa",
    "menu.selectionForeground": AZUL, "notifications.background": BRANCO,
    "notifications.foreground": TEXTO, "notifications.border": AZUL,
    "quickInput.background": BRANCO, "quickInputList.focusBackground": "#007a2e",
    "quickInputList.focusForeground": BRANCO, "scrollbarSlider.background": "#00277633",
    "scrollbarSlider.hoverBackground": "#00277666",
    "terminal.background": BRANCO, "terminal.foreground": TEXTO,
    "terminal.ansiGreen": VERDE_ESC, "terminal.ansiYellow": OURO, "terminal.ansiBlue": AZUL,
    "terminal.ansiRed": "#d32f2f", "terminal.ansiMagenta": "#7a3ea8", "terminal.ansiCyan": "#005f99",
    "gitDecoration.modifiedResourceForeground": OURO, "gitDecoration.addedResourceForeground": VERDE_ESC,
    "gitDecoration.untrackedResourceForeground": VERDE_ESC,
    "gitDecoration.deletedResourceForeground": "#d32f2f",
    "chat.requestBackground": "#e6eeff", "chat.slashCommandBackground": "#007a2e",
    "chat.slashCommandForeground": BRANCO, "inlineChat.background": BRANCO, "inlineChat.border": VERDE,
    "minimap.background": BRANCO, "minimap.selectionHighlight": "#ffdf00aa",
    "welcomePage.background": BRANCO, "commandCenter.background": "#1a3a8f",
    "commandCenter.foreground": BRANCO, "commandCenter.border": "#00000000",
}

def tok(name, scope, fg, style=None):
    s = {"foreground": fg}
    if style:
        s["fontStyle"] = style
    return {"name": name, "scope": scope, "settings": s}

TOKENS = [
    tok("Comment", ["comment", "punctuation.definition.comment"], "#4a5a7d", "italic"),
    tok("String", ["string", "punctuation.definition.string"], "#006b28"),
    tok("Number & constant", ["constant.numeric", "constant.language", "constant.character"], OURO),
    tok("Keyword", ["keyword", "storage", "storage.type", "keyword.control"], AZUL, "bold"),
    tok("Operator", ["keyword.operator"], "#7a5c00"),
    tok("Function", ["entity.name.function", "support.function", "meta.function-call"], "#006b28"),
    tok("Type / class", ["entity.name.type", "entity.name.class", "support.class", "support.type"], "#0a4fc4", "bold"),
    tok("Variable", ["variable", "variable.other"], TEXTO),
    tok("Parameter", ["variable.parameter"], "#7a5c00", "italic"),
    tok("Property", ["variable.other.property", "support.variable.property"], "#1a3a8f"),
    tok("Tag", ["entity.name.tag"], "#006b28"),
    tok("Attribute", ["entity.other.attribute-name"], "#7a5c00", "italic"),
    tok("Markup heading", ["markup.heading", "entity.name.section"], AZUL, "bold"),
    tok("Markup inline code", ["markup.inline.raw"], "#006b28"),
    tok("Self / this", ["variable.language"], "#7a5c00", "italic"),
    tok("Invalid", ["invalid"], "#d32f2f", "underline"),
]

def main():
    theme = {"name": "patriota claro", "type": "light", "colors": COLORS,
             "semanticHighlighting": True, "tokenColors": TOKENS}
    path = os.path.join("themes", "patriota-light-color-theme.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent="\t", ensure_ascii=False)
        f.write("\n")
    print(f"Gerado {path}")

if __name__ == "__main__":
    main()
