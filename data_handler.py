import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_data() -> dict:
    """Load all user data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_data(data: dict) -> None:
    """Save all user data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user_history(username: str) -> list:
    """Return feedback history for a specific user."""
    data = load_data()
    return data.get(username, [])


def save_feedback(username: str, mood: str, activity: str, liked: bool) -> None:
    """Append a feedback record for a user."""
    data = load_data()
    if username not in data:
        data[username] = []
    data[username].append({"mood": mood, "activity": activity, "liked": liked})
    save_data(data)


def is_returning_user(username: str) -> bool:
    """Check if the user has any stored history."""
    data = load_data()
    return username in data and len(data[username]) > 0


def get_all_users() -> list:
    """Return a list of all known usernames."""
    return list(load_data().keys())
