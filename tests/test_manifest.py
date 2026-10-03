import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_FILES = ["src/extension.js", "media/flag.js", "media/pet.js", "media/pet.css"]


def load_manifest():
    with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as f:
        return json.load(f)


def test_declared_files_exist():
    pkg = load_manifest()
    assert os.path.exists(os.path.join(ROOT, pkg["main"]))
    for theme in pkg["contributes"]["themes"]:
        assert os.path.exists(os.path.join(ROOT, theme["path"]))
    for views in pkg["contributes"]["views"].values():
        for view in views:
            assert os.path.exists(os.path.join(ROOT, view["icon"]))


def test_commands_have_titles():
    pkg = load_manifest()
    for cmd in pkg["contributes"]["commands"]:
        assert cmd["title"].startswith("Patriota")


def test_code_files_respect_line_limit():
    for rel in CODE_FILES:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            assert len(f.readlines()) <= 150, rel
