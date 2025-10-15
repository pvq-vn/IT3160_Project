import streamlit as st
from inference_engine import load_data, get_recommendations

# Tải dữ liệu một lần duy nhất khi ứng dụng khởi động
songs_db, rules_db = load_data()

st.title("MUSEEK 🎵")

# Tạo các lựa chọn cho người dùng
# (Bạn cần tự tạo danh sách các lựa chọn từ dữ liệu)
mood_options = ["Buồn", "Cô đơn", "Hoài niệm", "Lãng mạn", "Mơ mộng", "Mạnh mẽ", "Sôi động", "Thư giãn", "Vui vẻ", "Xúc động"]
activity_options = ["Hẹn hò", "Lái xe", "Lễ hội", "Nhớ kỷ niệm", "Party", "Suy ngẫm", "Tập trung", "Trẻ em"]
genre_options = ["Acoustic", "Ballad", "Country", "Dance", "EDM", "Hiphop", "K-Pop", "Latin", "OST", "Pop", "Quan họ", "R&B", "Rock", "V-Pop", "World music"]

# Lấy input từ người dùng
selected_mood = st.selectbox("Tâm trạng của bạn hôm nay là gì?", options=[""] + mood_options)
selected_activity = st.selectbox("Bạn đang làm gì?", options=[""] + activity_options)
selected_genre = st.selectbox("Thể loại bạn yêu thích?", options=[""] + genre_options)

# Nút để bắt đầu gợi ý
if st.button("Tìm nhạc cho tôi!"):
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
        # Gọi "bộ não" suy diễn
        recommendations = get_recommendations(user_input, songs_db, rules_db)

        if recommendations:
            st.success("Đây là những bài hát dành cho bạn:")
            for song_title, score in recommendations:
                st.write(f"**- {song_title}** (Điểm phù hợp: {score})")
        else:
            st.info("Rất tiếc, không tìm thấy bài hát nào phù hợp với lựa chọn của bạn.")