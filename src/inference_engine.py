import json

def load_data():
    """
    Tải dữ liệu từ các file JSON.
    Hàm này đọc cơ sở dữ liệu bài hát và cơ sở tri thức luật.
    """
    try:
        with open('data/songs.json', 'r', encoding='utf-8') as f:
            songs = json.load(f)
        with open('data/rules.json', 'r', encoding='utf-8') as f:
            rules = json.load(f)
        return songs, rules
    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy file {e.filename}. Hãy chắc chắn bạn chạy file từ thư mục gốc của project.")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Lỗi: File JSON không hợp lệ. Vui lòng kiểm tra lại cú pháp. Chi tiết: {e}")
        return None, None

def get_recommendations(user_input, songs, rules, top_n=5):
    """
    Hàm suy diễn chính để đưa ra gợi ý bài hát.

    Args:
        user_input (dict): Đầu vào từ người dùng, ví dụ: {"tam_trang": "Vui vẻ"}.
        songs (list): Danh sách tất cả bài hát từ songs.json.
        rules (list): Danh sách tất cả các luật từ rules.json.
        top_n (int): Số lượng bài hát gợi ý hàng đầu.

    Returns:
        list: Danh sách các tuple (tên bài hát, điểm số) được gợi ý.
    """
    if not songs or not rules:
        return []

    # 1. Khởi tạo điểm cho tất cả bài hát là 0
    song_scores = {song['title']: 0 for song in songs}

    # === GIAI ĐOẠN 1: SUY DIỄN BOTTOM-UP (ĐỐI SÁNH TRỰC TIẾP) ===
    # Cộng điểm trực tiếp nếu mood/activity của người dùng khớp với tag của bài hát.
    # Đây là bằng chứng mạnh nhất, nên có trọng số cao.
    
    user_mood = user_input.get('tam_trang')
    user_activity = user_input.get('hoat_dong')

    for song in songs:
        # Cộng 30 điểm nếu khớp tâm trạng
        if user_mood and user_mood in song.get('moods', []):
            song_scores[song['title']] += 30
        
        # Cộng 20 điểm nếu khớp hoạt động
        if user_activity and user_activity in song.get('activity', []):
            song_scores[song['title']] += 20

    # === GIAI ĐOẠN 2: SUY DIỄN TOP-DOWN (DỰA TRÊN LUẬT) ===
    # Áp dụng các luật chung để tinh chỉnh điểm số.
    
    for rule in rules:
        condition_key, condition_value = list(rule['condition'].items())[0]
        
        # Kiểm tra xem luật có được kích hoạt bởi đầu vào của người dùng không
        if condition_key in user_input and user_input[condition_key] == condition_value:
            effect = rule['effect']
            
            effect_type = effect['type']      # 'the_loai' hoặc 'nghe_si'
            effect_target = effect['target']  # 'Pop', 'Sơn Tùng M-TP', ...
            effect_score = effect['score']    # Điểm cộng/trừ

            # Áp dụng hiệu ứng của luật lên tất cả các bài hát
            for song in songs:
                # Xử lý cho thể loại (genre)
                if effect_type == 'the_loai':
                    # Kiểm tra xem thể loại mục tiêu có trong danh sách genre của bài hát không
                    if effect_target in song.get('genre', []):
                        song_scores[song['title']] += effect_score
                
                # Xử lý cho nghệ sĩ (artist)
                elif effect_type == 'nghe_si':
                    # Kiểm tra xem nghệ sĩ mục tiêu có trong danh sách artist của bài hát không
                    if effect_target in song.get('artist', []):
                        song_scores[song['title']] += effect_score

    # 3. Sắp xếp các bài hát theo điểm số từ cao đến thấp
    sorted_songs = sorted(song_scores.items(), key=lambda item: item[1], reverse=True)
    
    # 4. Trả về top_n bài hát có điểm cao nhất (và điểm > 0)
    final_recommendations = [(song, score) for song, score in sorted_songs if score > 0]
    return final_recommendations[:top_n]

# --- VÍ DỤ CÁCH SỬ DỤNG VÀ KIỂM THỬ ---
# File này có thể được import vào main.py hoặc chạy trực tiếp để test.
if __name__ == "__main__":
    songs_db, rules_db = load_data()
    
    if songs_db and rules_db:
        # Kịch bản 1: Người dùng vui vẻ và đang tiệc tùng
        print("="*30)
        my_input_1 = {
            "tam_trang": "Vui vẻ",
            "hoat_dong": "Party"
        }
        recommendations_1 = get_recommendations(my_input_1, songs_db, rules_db)
        print(f"Gợi ý cho bạn khi '{my_input_1['tam_trang']}' và đang '{my_input_1['hoat_dong']}':")
        if recommendations_1:
            for song, score in recommendations_1:
                print(f"- {song} (Điểm: {score})")
        else:
            print("Không tìm thấy gợi ý phù hợp.")

        # Kịch bản 2: Người dùng buồn và muốn suy ngẫm
        print("\n" + "="*30)
        my_input_2 = {
            "tam_trang": "Buồn",
            "hoat_dong": "Suy ngẫm"
        }
        recommendations_2 = get_recommendations(my_input_2, songs_db, rules_db)
        print(f"Gợi ý cho bạn khi '{my_input_2['tam_trang']}' và muốn '{my_input_2['hoat_dong']}':")
        if recommendations_2:
            for song, score in recommendations_2:
                print(f"- {song} (Điểm: {score})")
        else:
            print("Không tìm thấy gợi ý phù hợp.")
            
        # Kịch bản 3: Người dùng thích V-Pop
        print("\n" + "="*30)
        my_input_3 = {
            "the_loai_yeu_thich": "V-Pop"
        }
        recommendations_3 = get_recommendations(my_input_3, songs_db, rules_db)
        print(f"Gợi ý cho bạn khi bạn thích 'V-Pop':")
        if recommendations_3:
            for song, score in recommendations_3:
                print(f"- {song} (Điểm: {score})")
        else:
            print("Không tìm thấy gợi ý phù hợp.")