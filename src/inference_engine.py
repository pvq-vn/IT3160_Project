# mood_rules.py

def get_genres_by_mood(mood: str):
    mood = mood.lower().strip()
    rules = {
        "vui": ["pop", "dance", "electronic"],
        "buồn": ["acoustic", "sad", "ballad"],
        "thư giãn": ["lofi", "jazz", "chill"],
        "tập trung": ["instrumental", "classical"],
        "nhiệt huyết": ["rock", "hiphop", "edm"]
    }
    return rules.get(mood, [])
