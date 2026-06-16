import json
from pathlib import Path
from typing import Any

THEMES_DIR = Path("themes/").resolve()
TEMP_THEMES_DIR = Path("themes/tmp/").resolve()

FINAL_THEME = THEMES_DIR / "one-dark-pro-blur.json"
BASE_THEME = TEMP_THEMES_DIR / "base.json"
TEMP_THEMES = [
    theme
    for theme in TEMP_THEMES_DIR.iterdir()
    if theme.is_file() and theme.suffix == ".json" and theme != BASE_THEME
]

# ── Per-variant blur overrides ────────────────────────────────────────────────
# Keys match the theme name stem (after sync.sh runs theme_importer on them).
# bg = main editor bg at ~85% opacity (d9), surface = panel/sidebar bg at ~82% (d0).
# All transparent surfaces use 00 alpha so OS blur bleeds through.


def make_overrides(bg: str, surface: str) -> dict:
    return {
        "background.appearance": "blurred",
        "background": bg + "d9",
        "surface.background": surface + "d0",
        "editor.background": "#00000000",
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


def apply_blur(style: dict, theme_file: Path) -> dict:
    overrides = VARIANT_OVERRIDES.get(theme_file.stem)
    if overrides is None:
        print(f"  [warn] no blur overrides for '{theme_file.stem}', skipping")
        return style
    return {**style, **overrides}


def patch_theme_name(theme_file: Path) -> Any:
    json_data = json.loads(theme_file.read_text())
    json_data["name"] = theme_file.stem.replace("-", " ")
    return json_data


def main() -> None:
    base_theme_data = json.loads(BASE_THEME.read_text())

    for theme in TEMP_THEMES:
        patched_data = patch_theme_name(theme)
        del patched_data["$schema"]

        if "style" in patched_data:
            patched_data["style"] = apply_blur(patched_data["style"], theme)
        else:
            print(f"  [warn] no 'style' key in {theme.stem}")

        base_theme_data["themes"].append(patched_data)

    FINAL_THEME.write_text(json.dumps(base_theme_data, indent=4))


if __name__ == "__main__":
    main()
