# src/recommender.py
from src.inference_engine import load_data, get_recommendations

class Recommender:
    def __init__(self):
        """Khởi tạo và tải dữ liệu."""
        self.songs_db, self.rules_db = load_data()
        if self.songs_db is None or self.rules_db is None:
            raise RuntimeError("Không thể tải dữ liệu cho hệ thống gợi ý.")

    def suggest(self, user_input, top_n=5):
        """
        Nhận đầu vào và trả về danh sách gợi ý.
        Đây là hàm duy nhất mà giao diện người dùng (app.py) cần biết đến.
        """
        if not user_input:
            return []
        
        return get_recommendations(user_input, self.songs_db, self.rules_db, top_n)