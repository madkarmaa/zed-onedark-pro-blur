import json
from pathlib import Path

THEMES_DIR = Path("themes/").resolve()
TEMP_THEMES_DIR = Path("themes/tmp/").resolve()

FINAL_THEME = THEMES_DIR / "onedark-pro-blur.json"
BASE_THEME = TEMP_THEMES_DIR / "base.json"
TEMP_THEMES = [
    theme
    for theme in TEMP_THEMES_DIR.iterdir()
    if theme.is_file() and theme.suffix == ".json" and theme != BASE_THEME
]


def make_overrides(bg: str, surface: str) -> dict:
    return {
        "background.appearance": "blurred",
        "background": bg + "d9",
        "surface.background": surface + "d0",
        "editor.background": "#00000000",  # "editor.background": bg + "d9", # matches more closely to base theme but loses blur effect
        "tab_bar.background": "#00000000",
        "toolbar.background": "#00000000",
        "panel.background": "#00000000",
        "terminal.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "editor.active_line.background": bg + "60",
    }


VARIANT_OVERRIDES = {
    "OneDark-Pro": make_overrides("#282c34", "#21252b"),
    "OneDark-Pro-flat": make_overrides("#282c34", "#282c34"),
    "OneDark-Pro-mix": make_overrides("#282c34", "#21252b"),
    "OneDark-Pro-darker": make_overrides("#23272e", "#1e2227"),
    "OneDark-Pro-night-flat": make_overrides("#16191d", "#16191d"),
}

SYNTAX_OVERRIDES = {
    "property": {"color": "#e06c75", "font_style": None, "font_weight": None},
    "boolean": {"color": "#56b6c2", "font_style": None, "font_weight": None},
    "enum": {"color": "#d19a66", "font_style": None, "font_weight": None},
    "label": {"color": "#e06c75", "font_style": None, "font_weight": None},
    "link_text": {"color": "#61afef", "font_style": None, "font_weight": None},
    "link_uri": {"color": "#c678dd", "font_style": None, "font_weight": None},
    "preproc": {"color": "#c678dd", "font_style": None, "font_weight": None},
    "punctuation": {"color": "#abb2bf", "font_style": None, "font_weight": None},
    "punctuation.bracket": {
        "color": "#abb2bf",
        "font_style": None,
        "font_weight": None,
    },
    "punctuation.delimiter": {
        "color": "#abb2bf",
        "font_style": None,
        "font_weight": None,
    },
    "punctuation.list_marker": {
        "color": "#e06c75",
        "font_style": None,
        "font_weight": None,
    },
    "punctuation.special": {
        "color": "#c678dd",
        "font_style": None,
        "font_weight": None,
    },
    "title": {"color": "#e06c75", "font_style": None, "font_weight": None},
}


def apply_syntax_overrides(theme_data: dict) -> dict:
    style = theme_data.get("style", {})
    syntax = style.get("syntax", {})

    for token, value in SYNTAX_OVERRIDES.items():
        syntax[token] = value

    style["syntax"] = syntax
    theme_data["style"] = style
    return theme_data


def apply_blur(style: dict, theme_file: Path) -> dict:
    overrides = VARIANT_OVERRIDES.get(theme_file.stem)
    if overrides is None:
        return style
    return {**style, **overrides}


def patch_theme_name(theme_file: Path) -> str:
    return theme_file.stem.replace("-", " ") + " (blur)"


def main() -> None:
    base_theme_data = json.loads(BASE_THEME.read_text())

    for theme in TEMP_THEMES:
        json_data = json.loads(theme.read_text())

        del json_data["$schema"]

        json_data["name"] = patch_theme_name(theme)

        if "style" in json_data:
            json_data["style"] = apply_blur(json_data["style"], theme)
            json_data = apply_syntax_overrides(json_data)

        base_theme_data["themes"].append(json_data)

    FINAL_THEME.write_text(json.dumps(base_theme_data, indent=4))


if __name__ == "__main__":
    main()
