import json
import os

# Lấy đường dẫn tuyệt đối đến thư mục gốc của project
# __file__ là đường dẫn đến file hiện tại (inference_engine.py)
# os.path.dirname() sẽ lấy thư mục chứa file đó (tức là 'src')
# os.path.join(..., '..') sẽ đi lùi một cấp, ra đến thư mục gốc
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_data(songs_path=None, rules_path=None):
    """Tải dữ liệu từ các file JSON bằng đường dẫn tuyệt đối."""
    
    # Nếu không cung cấp đường dẫn, tự động tìm trong thư mục data
    if songs_path is None:
        songs_path = os.path.join(PROJECT_ROOT, 'data', 'songs.json')
    if rules_path is None:
        rules_path = os.path.join(PROJECT_ROOT, 'data', 'rules.json')
    
    try:
        with open(songs_path, 'r', encoding='utf-8') as f:
            songs = json.load(f)
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)
        return songs, rules
    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy file tại đường dẫn: {e.filename}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Lỗi: File JSON không hợp lệ. Vui lòng kiểm tra lại cú pháp. Chi tiết: {e}")
        return None, None

def get_recommendations(user_input, songs, rules, top_n=5):
    """Hàm suy diễn chính để đưa ra gợi ý bài hát."""
    if not songs or not rules:
        return []

    song_scores = {song['title']: 0 for song in songs}

    # === Giai đoạn 1: Suy diễn Bottom-up (Đối sánh trực tiếp) ===
    user_mood = user_input.get('tam_trang')
    user_activity = user_input.get('hoat_dong')

    for song in songs:
        if user_mood and user_mood in song.get('moods', []):
            song_scores[song['title']] += 30
        if user_activity and user_activity in song.get('activity', []):
            song_scores[song['title']] += 20

    # === Giai đoạn 2: Suy diễn Top-down (Dựa trên luật) ===
    for rule in rules:
        condition_key, condition_value = list(rule['condition'].items())[0]
        
        if condition_key in user_input and user_input[condition_key] == condition_value:
            effect = rule['effect']
            effect_type = effect['type']
            effect_target = effect['target']
            effect_score = effect['score']

            for song in songs:
                # Xử lý cho thể loại (genre)
                if effect_type == 'the_loai':
                    if effect_target in song.get('genre', []):
                        song_scores[song['title']] += effect_score
                
                # Xử lý cho nghệ sĩ (artist)
                elif effect_type == 'nghe_si':
                    # Artist có thể là list hoặc string, cần xử lý cả 2
                    artist_field = song.get('artist', [])
                    if isinstance(artist_field, list):
                        if effect_target in artist_field:
                            song_scores[song['title']] += effect_score
                    elif isinstance(artist_field, str):
                        if effect_target == artist_field:
                             song_scores[song['title']] += effect_score

    # Sắp xếp và trả về kết quả
    sorted_songs = sorted(song_scores.items(), key=lambda item: item[1], reverse=True)
    final_recommendations = [(song, score) for song, score in sorted_songs if score > 0]
    return final_recommendations[:top_n]