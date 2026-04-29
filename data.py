"""Data module providing mood metadata and constants."""

from utils import MOOD_EMOJI, MOOD_COLOR, MOOD_BG
from model import MOOD_ACTIVITIES, MOOD_KEYWORDS

# Combined mood metadata
MOOD_META = {
    mood: {
        "label": mood.capitalize(),
        "emoji": MOOD_EMOJI.get(mood, "🙂"),
        "color": MOOD_COLOR.get(mood, "#888"),
        "bg": MOOD_BG.get(mood, "#FAFAFA"),
        "activities": MOOD_ACTIVITIES.get(mood, []),
        "keywords": MOOD_KEYWORDS.get(mood, []),
    }
    for mood in MOOD_EMOJI.keys()
}
