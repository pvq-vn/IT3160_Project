# recommender.py
import json
import random
from .inference_engine import get_genres_by_mood

def load_songs(path="data/songs.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def recommend_songs(mood, num_songs=5):
    songs = load_songs()
    genres = get_genres_by_mood(mood)

    if not genres:
        return []

    candidates = [s for s in songs if s.get("genre", "").lower() in genres]
    random.shuffle(candidates)
    return candidates[:num_songs]
