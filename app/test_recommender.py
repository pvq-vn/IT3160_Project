import json
from pathlib import Path

# Đường dẫn đến thư mục gốc (tự động xác định)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA = BASE_DIR / "data" / "songs.json"
RULES = BASE_DIR / "data" / "rules.json"

def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

songs = load_json(DATA)
rules = load_json(RULES)

def recommend(mood):
    """Gợi ý bài hát dựa trên tâm trạng"""
    rec_ids = set()
    for rule in rules:
        if rule.get("mood") == mood:
            rec_ids.update(rule.get("id", []))

    # Lọc danh sách bài hát theo ID đã được gợi ý
    return [s for s in songs if s["id"] in rec_ids]

# --- Test thử ---
if __name__ == "__main__":
    mood_input = input("Nhập tâm trạng (vui / buồn / năng động): ")
    recs = recommend(mood_input)
    if not recs:
        print("Không tìm thấy gợi ý phù hợp.")
    else:
        print("🎵 Gợi ý bài hát cho tâm trạng", mood_input, ":")
        for s in recs:
            print(f"- {s['title']} ({s['artist']}) - {s['genre']}")
