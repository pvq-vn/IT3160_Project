# src/app.py
import streamlit as st
from src.recommender import Recommender

st.set_page_config(page_title="Music Recommender", layout="centered")

@st.cache_resource
def load_recommender():
    """Tải mô hình recommender và cache lại để không phải load lại mỗi lần."""
    try:
        return Recommender()
    except RuntimeError as e:
        st.error(e)
        return None

recommender_system = load_recommender()

st.title("Hệ thống Gợi ý Âm nhạc 🎵")
st.write("Dựa trên Biểu diễn tri thức và Suy diễn logic")

if recommender_system:
    # Lấy các tùy chọn từ DB để điền vào selectbox
    mood_options = sorted(list(set(mood for song in recommender_system.songs_db for mood in song.get('moods', []))))
    activity_options = sorted(list(set(act for song in recommender_system.songs_db for act in song.get('activity', []))))
    genre_options = sorted(list(set(g for song in recommender_system.songs_db for g in song.get('genre', []))))

    # Giao diện
    selected_mood = st.selectbox("Tâm trạng của bạn là gì?", options=[""] + mood_options)
    selected_activity = st.selectbox("Bạn đang làm gì?", options=[""] + activity_options)
    selected_genre = st.selectbox("Bạn có yêu thích thể loại cụ thể nào không?", options=[""] + genre_options)

    if st.button("Tìm nhạc cho tôi!", use_container_width=True):
        user_input = {}
        if selected_mood:
            user_input["tam_trang"] = selected_mood
        if selected_activity:
            user_input["hoat_dong"] = selected_activity
        if selected_genre:
            user_input["the_loai_yeu_thich"] = selected_genre

        if not user_input:
            st.warning("Vui lòng chọn ít nhất một tiêu chí.")
        else:
            with st.spinner("Đang tìm kiếm những giai điệu phù hợp..."):
                recommendations = recommender_system.suggest(user_input)

                if recommendations:
                    st.success("Đây là những bài hát dành cho bạn:")
                    for i, (song_title, score) in enumerate(recommendations):
                        st.write(f"{i+1}. **{song_title}** (Điểm phù hợp: {score})")
                else:
                    st.info("Rất tiếc, không tìm thấy bài hát nào phù hợp với lựa chọn của bạn.")