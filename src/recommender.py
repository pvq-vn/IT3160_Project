# src/recommender.py

# ĐÃ SỬA: Dùng import tương đối (dấu chấm) để gọi file cùng cấp
from .inference_engine import load_data, get_recommendations

class Recommender:
    def __init__(self):
        """Khởi tạo và tải dữ liệu."""
        self.songs_db, self.rules_db = load_data()
        if self.songs_db is None or self.rules_db is None:
            raise RuntimeError("Không thể tải dữ liệu cho hệ thống gợi ý. Hãy kiểm tra lại đường dẫn file trong 'inference_engine.py'.")

    def suggest(self, user_input, top_n=5):
        """Hàm chính để đưa ra gợi ý."""
        if not user_input:
            return []
        
        return get_recommendations(user_input, self.songs_db, self.rules_db, top_n)