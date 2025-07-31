themes = {
    "Light Green": {"bg": "#d0f0c0", "fg": "black"},
    "Dark Mode": {"bg": "#2e2e2e", "fg": "white"},
    "Sky Blue": {"bg": "#add8e6", "fg": "black"}
}

def apply_theme(root, theme_name):
    theme = themes.get(theme_name, themes["Light Green"])
    root.configure(bg=theme["bg"])
    return theme
