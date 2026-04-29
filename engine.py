"""Engine module - real ML version."""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from data_handler import (
    load_data,
    save_data,
    get_user_history,
)

from model import MOOD_ACTIVITIES


# ─────────────────────────────────────────
# TRAINING DATA
# ─────────────────────────────────────────
TRAIN_DATA = [
    ("happy", "happy"),
    ("I feel happy and amazing", "happy"),
    ("this is a great day", "happy"),
    ("I feel joyful and cheerful", "happy"),
    ("I am in a good mood", "happy"),

    ("excited", "excited"),
    ("I am very excited", "excited"),
    ("I feel thrilled and energetic", "excited"),
    ("I am pumped and ready", "excited"),
    ("I feel enthusiastic", "excited"),

    ("sad", "sad"),
    ("I feel sad and down", "sad"),
    ("I feel lonely", "sad"),
    ("I am unhappy today", "sad"),
    ("I feel low and empty", "sad"),

    ("anxious", "anxious"),
    ("I feel anxious", "anxious"),
    ("I have anxiety", "anxious"),
    ("I feel nervous and worried", "anxious"),
    ("I feel panicked and uneasy", "anxious"),

    ("bored", "bored"),
    ("I am bored", "bored"),
    ("nothing to do", "bored"),
    ("I feel dull and uninterested", "bored"),

    ("tired", "tired"),
    ("I am tired", "tired"),
    ("I feel exhausted", "tired"),
    ("I feel sleepy and drained", "tired"),

    ("angry", "angry"),
    ("I am angry", "angry"),
    ("I feel frustrated", "angry"),
    ("I am mad and irritated", "angry"),

    ("stressed", "stressed"),
    ("I am stressed", "stressed"),
    ("too much pressure", "stressed"),
    ("I feel overwhelmed by work", "stressed"),
]


DIRECT_MOOD_ALIASES = {
    "happy": ["happy", "joyful", "cheerful", "great", "amazing"],
    "sad": ["sad", "lonely", "unhappy", "depressed", "low"],
    "anxious": ["anxious", "anxiety", "nervous", "worried", "panic", "panicked"],
    "bored": ["bored", "boring", "dull", "uninterested"],
    "tired": ["tired", "exhausted", "sleepy", "drained", "fatigue"],
    "angry": ["angry", "mad", "furious", "frustrated", "irritated"],
    "excited": ["excited", "thrilled", "pumped", "energetic", "enthusiastic", "hyped"],
    "stressed": ["stressed", "stress", "overwhelmed", "pressure", "swamped"],
}


# ─────────────────────────────────────────
# MOOD CLASSIFIER
# ─────────────────────────────────────────
class MoodClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False

    def train(self):
        texts = [text for text, _ in TRAIN_DATA]
        labels = [label for _, label in TRAIN_DATA]

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

        self.is_trained = True
        return self

    def _direct_mood_match(self, text: str):
        words = set(re.findall(r"[a-zA-Z']+", text.lower()))

        for mood, aliases in DIRECT_MOOD_ALIASES.items():
            if any(alias in words for alias in aliases):
                return mood

        return None

    def predict(self, text: str):
        if not self.is_trained:
            self.train()

        X = self.vectorizer.transform([text])
        pred = self.model.predict(X)[0]

        probs = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        confidence = {
            classes[i]: float(probs[i])
            for i in range(len(classes))
        }

        direct_mood = self._direct_mood_match(text)
        if direct_mood in confidence:
            confidence = self._boost_direct_confidence(confidence, direct_mood)
            pred = direct_mood

        confidence = dict(
            sorted(confidence.items(), key=lambda item: item[1], reverse=True)
        )

        return pred, confidence

    @staticmethod
    def _boost_direct_confidence(confidence: dict, mood: str):
        boosted = {}
        remaining = 0.15
        other_total = sum(value for key, value in confidence.items() if key != mood)

        for key, value in confidence.items():
            if key == mood:
                boosted[key] = 0.85
            elif other_total:
                boosted[key] = remaining * (value / other_total)
            else:
                boosted[key] = remaining / max(len(confidence) - 1, 1)

        return boosted


# ─────────────────────────────────────────
# USER MEMORY
# ─────────────────────────────────────────
class UserMemory:

    def get_or_create_user(self, username: str):
        data = load_data()
        is_new = username not in data

        if is_new:
            data[username] = []
            save_data(data)

        return username, is_new

    def total_sessions(self, uid: str):
        history = get_user_history(uid)
        return len([h for h in history if h.get("input")])

    def liked_actions(self, uid: str):
        history = get_user_history(uid)
        return [
            h for h in history
            if h.get("type") == "feedback" and h.get("liked") is True
        ]

    def mood_frequency(self, uid: str):
        history = get_user_history(uid)
        freq = {}

        for h in history:
            mood = h.get("mood")
            if not mood:
                continue
            freq[mood] = freq.get(mood, 0) + 1

        return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    def recent_history(self, uid: str, count=6):
        history = get_user_history(uid)
        mood_entries = [h for h in history if h.get("input")]
        return mood_entries[-count:]

    def record_feedback(self, uid, aid, mood, action):
        data = load_data()

        if uid not in data:
            data[uid] = []

        data[uid].append({
            "type": "feedback",
            "mood": mood,
            "activity": aid,
            "liked": action == "liked",
        })

        save_data(data)

    def record_mood(self, uid, mood, text):
        data = load_data()

        if uid not in data:
            data[uid] = []

        data[uid].append({
            "type": "mood",
            "mood": mood,
            "input": text,
        })

        save_data(data)


# ─────────────────────────────────────────
# RECOMMENDATION ENGINE
# ─────────────────────────────────────────
class RecommendationEngine:

    def __init__(self, user_memory):
        self.memory = user_memory

    def get_recommendations(self, uid, mood, n=3):
        activities = MOOD_ACTIVITIES.get(mood, [])
        history = get_user_history(uid)

        feedback_entries = [
            h for h in history
            if h.get("type") == "feedback" and h.get("activity")
        ]

        liked = {
            h["activity"]
            for h in feedback_entries
            if h.get("liked") is True
        }

        disliked = {
            h["activity"]
            for h in feedback_entries
            if h.get("liked") is False
        }

        scored = []

        for idx, activity in enumerate(activities):
            modifier = 0.0

            if activity in liked:
                modifier += 1.5

            if activity in disliked:
                modifier -= 1.0

            score = 5.0 + modifier

            if activity in liked:
                tag = "Previously loved"
            elif activity in disliked:
                tag = "Trying something different"
            else:
                tag = ""

            scored.append({
                "id": activity,
                "action": activity,
                "category": "Suggestion",
                "score": score,
                "modifier": modifier,
                "tag": tag,
                "original_order": idx,
            })

        ranked = sorted(
            scored,
            key=lambda item: (item["score"], -item["original_order"]),
            reverse=True,
        )

        return ranked[:n]
