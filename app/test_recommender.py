import unittest
# Vì file test nằm cùng cấp với thư mục src, chúng ta có thể import trực tiếp
from src.recommender import Recommender

class TestRecommender(unittest.TestCase):
    """
    Đây là một class kiểm thử, nó bắt buộc phải kế thừa từ unittest.TestCase
    """
    recommender_system = None

    @classmethod
    def setUpClass(cls):
        """Tải dữ liệu một lần duy nhất trước khi tất cả các test bắt đầu."""
        print("Đang tải dữ liệu cho bộ test...")
        cls.recommender_system = Recommender()
        print("Tải dữ liệu thành công.")

    def test_suggest_for_sad_mood(self):
        """
        Hàm này là một bài test vì tên của nó bắt đầu bằng 'test_'.
        Nó kiểm tra gợi ý cho tâm trạng 'Buồn'.
        """
        print("\n[TEST] Gợi ý cho tâm trạng 'Buồn'")
        user_input = {"tam_trang": "Buồn"}
        recommendations = self.recommender_system.suggest(user_input)
        
        # 1. Kiểm tra phải có kết quả trả về
        self.assertTrue(len(recommendations) > 0, "Phải trả về ít nhất một gợi ý khi buồn")
        
        # 2. Kiểm tra xem bài hát có điểm cao nhất có phải là một bài Ballad không
        top_song_title = recommendations[0][0]
        top_song_data = next((song for song in self.recommender_system.songs_db if song['title'] == top_song_title), None)
        
        self.assertIn("Ballad", top_song_data['genre'], f"Bài hát '{top_song_title}' nên là Ballad khi buồn.")
        print("=> PASS: Gợi ý cho tâm trạng buồn hoạt động đúng.")

    def test_suggest_for_party(self):
        """
        Hàm này cũng là một bài test vì tên của nó bắt đầu bằng 'test_'.
        Nó kiểm tra gợi ý cho hoạt động 'Party'.
        """
        print("\n[TEST] Gợi ý cho hoạt động 'Party'")
        user_input = {"hoat_dong": "Party"}
        recommendations = self.recommender_system.suggest(user_input)
        
        self.assertTrue(len(recommendations) > 0, "Phải trả về ít nhất một gợi ý khi Party")
        
        top_song_title = recommendations[0][0]
        top_song_data = next((song for song in self.recommender_system.songs_db if song['title'] == top_song_title), None)
        
        is_dance_or_edm = any(genre in ["Dance", "EDM"] for genre in top_song_data['genre'])
        self.assertTrue(is_dance_or_edm, f"Bài hát '{top_song_title}' nên là Dance/EDM khi Party.")
        print("=> PASS: Gợi ý cho hoạt động Party hoạt động đúng.")

# Dòng này cho phép bạn chạy file trực tiếp bằng `python test_recommender.py`
# hoặc chạy qua `python -m unittest discover`
if __name__ == '__main__':
    unittest.main(verbosity=2)