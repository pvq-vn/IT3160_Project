import streamlit as st
import json
from pathlib import Path

# --- Đọc dữ liệu ---
BASE_DIR = Path(__file__).resolve().parents[1]  # cha của src/
DATA = BASE_DIR / "data" / "songs.json"
RULES = BASE_DIR / "data" / "rules.json"

def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

songs = load_json(DATA)
rules = load_json(RULES)

def recommend(mood):
    rec_ids = set()
    for rule in rules:
        if rule.get("mood") == mood:
            rec_ids.update(rule.get("id", []))
    return [s for s in songs if s["id"] in rec_ids]

# --- Giao diện Streamlit ---
st.title("🎶 Hệ gợi ý nhạc đơn giản (Rule-based)")

mood = st.selectbox(
    "Chọn tâm trạng của bạn:",
    ["vui", "buồn", "năng động"]
)

if st.button("Gợi ý nhạc"):
    recs = recommend(mood)
    if not recs:
        st.warning("Không tìm thấy bài hát phù hợp.")
    else:
        st.success(f"Gợi ý bài hát cho tâm trạng '{mood}':")
        for s in recs:
            st.write(f"🎵 **{s['title']}** – {s['artist']} ({s['genre']})")
