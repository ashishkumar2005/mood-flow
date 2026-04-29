"""Utility helpers for Mood Flow."""

MOOD_EMOJI: dict[str, str] = {
    "happy":   "😊",
    "sad":     "😢",
    "anxious": "😰",
    "bored":   "😑",
    "tired":   "😴",
    "angry":   "😠",
    "excited": "🤩",
    "stressed": "😤",
}

MOOD_COLOR: dict[str, str] = {
    "happy":   "#FFD166",
    "sad":     "#6AAFE6",
    "anxious": "#EF8C8C",
    "bored":   "#B5B5B5",
    "tired":   "#A89CC8",
    "excited": "#06D6A0",
    "angry":   "#EF233C",
    "stressed": "#F4845F",
}

MOOD_BG: dict[str, str] = {
    "happy":   "#FFFBEA",
    "sad":     "#EBF4FD",
    "anxious": "#FDF0F0",
    "bored":   "#F5F5F5",
    "tired":   "#F3F0FA",
    "excited": "#EDFAF5",
    "angry":   "#FEE8EC",
    "stressed": "#FEF0EB",
}


def mood_emoji(mood: str) -> str:
    return MOOD_EMOJI.get(mood, "🙂")


def mood_color(mood: str) -> str:
    return MOOD_COLOR.get(mood, "#888")


def mood_bg(mood: str) -> str:
    return MOOD_BG.get(mood, "#FAFAFA")


def capitalize_name(name: str) -> str:
    return name.strip().title() if name.strip() else "Friend"


def feedback_key(username: str, mood: str, activity: str, index: int) -> str:
    """Unique session-state key for a feedback pair."""
    safe = activity.replace(" ", "_").replace("/", "-")
    return f"fb_{username}_{mood}_{safe}_{index}"
