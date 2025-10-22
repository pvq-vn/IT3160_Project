# test/test_recommender.py

import unittest
import sys
import os

# Thêm thư mục gốc vào đường dẫn để Python tìm thấy 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommender import Recommender

class TestRecommender(unittest.TestCase):
    recommender_system = None

    @classmethod
    def setUpClass(cls):
        """Tải dữ liệu một lần duy nhất."""
        cls.recommender_system = Recommender()

    def test_suggest_for_sad_mood(self):
        """Kiểm tra gợi ý cho tâm trạng 'Buồn'."""
        user_input = {"tam_trang": "Buồn"}
        recommendations = self.recommender_system.suggest(user_input)
        
        self.assertTrue(len(recommendations) > 0, "Phải trả về ít nhất một gợi ý khi buồn")
        
        top_song_title = recommendations[0][0]
        top_song_data = next((song for song in self.recommender_system.songs_db if song['title'] == top_song_title), None)
        
        self.assertIn("Ballad", top_song_data['genre'], f"Bài hát '{top_song_title}' nên là Ballad khi buồn.")

    def test_suggest_for_party(self):
        """Kiểm tra gợi ý cho hoạt động 'Party'."""
        user_input = {"hoat_dong": "Party"}
        recommendations = self.recommender_system.suggest(user_input)
        
        self.assertTrue(len(recommendations) > 0, "Phải trả về ít nhất một gợi ý khi Party")
        
        top_song_title = recommendations[0][0]
        top_song_data = next((song for song in self.recommender_system.songs_db if song['title'] == top_song_title), None)
        
        is_dance_or_edm = any(genre in ["Dance", "EDM"] for genre in top_song_data['genre'])
        self.assertTrue(is_dance_or_edm, f"Bài hát '{top_song_title}' nên là Dance/EDM khi Party.")

if __name__ == '__main__':
    unittest.main(verbosity=2)