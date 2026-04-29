from collections import defaultdict
from data_handler import get_user_history

# ── Rule-based activity bank ────────────────────────────────────────────────
MOOD_ACTIVITIES: dict[str, list[str]] = {
    "happy": [
        "Go for a nature walk 🌿",
        "Call a friend you miss 📞",
        "Start a creative project 🎨",
        "Cook your favourite meal 🍳",
        "Write in a gratitude journal ✍️",
        "Listen to an upbeat playlist 🎵",
        "Explore a new neighbourhood 🗺️",
        "Teach someone a skill you love 🏫",
    ],
    "sad": [
        "Watch a comforting movie 🎬",
        "Take a warm shower 🚿",
        "Read an inspiring book 📚",
        "Cuddle with a pet 🐾",
        "Write down your feelings 📝",
        "Listen to calming music 🎶",
        "Reach out to a trusted friend 💬",
        "Do gentle stretching 🧘",
    ],
    "anxious": [
        "Try box-breathing for 5 minutes 🌬️",
        "Go for a brisk walk outside 🚶",
        "Tidy up your space 🧹",
        "Write a brain-dump list 📋",
        "Watch a lighthearted comedy 😂",
        "Practice progressive muscle relaxation 💪",
        "Limit screen time for an hour 📵",
        "Make a warm herbal tea ☕",
    ],
    "bored": [
        "Learn something new on YouTube 🎓",
        "Pick up a puzzle or board game 🧩",
        "Try a new recipe 🥗",
        "Sketch or doodle freely ✏️",
        "Rearrange your room 🪑",
        "Start a short online course 💻",
        "Write a short story or poem 📖",
        "Explore a podcast you've never heard 🎙️",
    ],
    "tired": [
        "Take a power nap (20 min) 😴",
        "Do gentle yoga 🧘",
        "Make a nourishing smoothie 🥤",
        "Watch something light & funny 😄",
        "Sit outside and breathe fresh air 🌤️",
        "Read a light magazine or blog 📰",
        "Take a short walk to reset 🚶",
        "Hydrate and have a healthy snack 🍎",
    ],
    "angry": [
        "Go for an intense run 🏃",
        "Punch a pillow or do push-ups 🥊",
        "Write an unsent letter 📨",
        "Listen to loud energising music 🎸",
        "Vent to a close friend 🗣️",
        "Channel rage into cleaning 🧽",
        "Try cold water on your face 💦",
        "Doodle or colour something chaotic 🎨",
    ],
    "excited": [
        "Channel energy into a side project 🚀",
        "Plan something you've been putting off 📅",
        "Share good news with someone 🎉",
        "Start a vision board 🖼️",
        "Dance it out 💃",
        "Write down your big dreams 🌟",
        "Celebrate with your favourite treat 🍰",
        "Reach out and inspire others ✨",
    ],
    "stressed": [
        "Prioritise your to-do list 📋",
        "Try the 5-4-3-2-1 grounding technique 🌱",
        "Do a 10-minute meditation 🧘",
        "Step outside for fresh air 🌬️",
        "Declutter one small area 📦",
        "Talk to someone you trust 💬",
        "Exercise to burn off cortisol 🏋️",
        "Limit caffeine and drink water 💧",
    ],
}

# Keyword → mood mapping for fuzzy detection
MOOD_KEYWORDS: dict[str, list[str]] = {
    "happy":   ["happy", "great", "joy", "good", "wonderful", "amazing", "fantastic", "cheerful", "elated"],
    "sad":     ["sad", "down", "unhappy", "depressed", "blue", "melancholy", "grief", "cry", "lonely", "empty"],
    "anxious": ["anxious", "worried", "nervous", "panic", "stress", "tense", "uneasy", "afraid", "scared", "fear"],
    "bored":   ["bored", "boring", "dull", "nothing to do", "uninterested", "restless", "idle", "monotonous"],
    "tired":   ["tired", "exhausted", "sleepy", "fatigue", "drained", "worn out", "weary", "drowsy", "lethargic"],
    "angry":   ["angry", "mad", "furious", "irritated", "annoyed", "rage", "frustrated", "upset", "livid"],
    "excited": ["excited", "thrilled", "pumped", "energetic", "enthusiastic", "hyped", "eager", "stoked"],
    "stressed": ["stressed", "overwhelmed", "pressure", "burned out", "overloaded", "frantic", "swamped"],
}


def detect_mood(mood_input: str) -> str:
    """Map free-text mood input to a canonical mood label."""
    text = mood_input.lower()
    scores: dict[str, int] = defaultdict(int)
    for mood, keywords in MOOD_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[mood] += 1
    if scores:
        return max(scores, key=lambda m: scores[m])
    return "happy"   # safe default


def _base_suggestions(mood: str) -> list[str]:
    """Return the rule-based activity list for a mood."""
    return list(MOOD_ACTIVITIES.get(mood, MOOD_ACTIVITIES["happy"]))


def _score_activities(activities: list[str], history: list[dict], mood: str) -> dict[str, float]:
    """
    Score every activity using past feedback.

    Scoring rules
    -------------
    • Base score = 1.0 for each activity
    • +0.5  for every 👍 the user gave THIS activity in the SAME mood
    • -0.4  for every 👎 the user gave THIS activity in the SAME mood
    • +0.2  for every 👍 the user gave THIS activity in a DIFFERENT mood
      (cross-mood positive signal, discounted)
    """
    scores: dict[str, float] = {act: 1.0 for act in activities}

    for record in history:
        act = record.get("activity", "")
        liked = record.get("liked", False)
        same_mood = record.get("mood", "") == mood

        if act not in scores:
            continue

        if liked:
            scores[act] += 0.5 if same_mood else 0.2
        else:
            scores[act] -= 0.4 if same_mood else 0.1

    return scores


def get_recommendations(mood_input: str, username: str, top_n: int = 4) -> tuple[str, list[str]]:
    """
    Return (detected_mood, ranked_activity_list).

    Steps
    -----
    1. Detect canonical mood from free text.
    2. Pull base activity list.
    3. Score with user feedback (personalization).
    4. Sort descending and return top_n.
    """
    from data_handler import get_user_history  # local import to avoid circular refs

    mood = detect_mood(mood_input)
    activities = _base_suggestions(mood)
    history = get_user_history(username)

    scores = _score_activities(activities, history, mood)
    ranked = sorted(activities, key=lambda a: scores[a], reverse=True)

    return mood, ranked[:top_n]


def get_analytics(username: str) -> dict:
    """Compute simple analytics for the sidebar."""
    history = get_user_history(username)
    if not history:
        return {}

    total = len(history)
    liked = sum(1 for r in history if r["liked"])
    disliked = total - liked

    mood_counts: dict[str, int] = defaultdict(int)
    for r in history:
        mood_counts[r["mood"]] += 1

    activity_likes: dict[str, int] = defaultdict(int)
    for r in history:
        if r["liked"]:
            activity_likes[r["activity"]] += 1

    top_activity = max(activity_likes, key=lambda a: activity_likes[a]) if activity_likes else None

    return {
        "total_sessions": total,
        "liked": liked,
        "disliked": disliked,
        "mood_counts": dict(mood_counts),
        "top_activity": top_activity,
    }
