from flask import Blueprint, render_template, session, request
from app.services.chart_service import get_popular_songs, get_today_popular_posts
from app.services.profile_service import users_collection, add_liked_song

chart_bp = Blueprint('chart', __name__)

@chart_bp.route('/chart')
def chart_page():
    # 인기곡/오늘 인기 게시글 조회
    popular_songs = get_popular_songs()
    daily_posts = get_today_popular_posts()
    
    # 로그인 상태, 사용자가 좋아요 누른 곡 표시
    if 'user_id' in session:
        user_data = users_collection.find_one({"username": session['user_id']})
        liked_track_ids = set()
        if user_data and 'like_music' in user_data:
            liked_track_ids = {song.get('track_id') for song in user_data['like_music']}

        for song in popular_songs:
            song['is_liked'] = song.get('id') in liked_track_ids
    
    # 차트 템플릿 렌더링
    return render_template(
        'chart.html',
        popular_songs=popular_songs,
        daily_posts=daily_posts
    )

# 좋아요 처리 API
@chart_bp.route('/like', methods=['POST'])
def like_song_from_chart():
    if 'user_id' not in session:
        return {"success": False, "message": "로그인이 필요합니다."}, 401
    
    username = session['user_id']
    song_data = request.json
    
    response, status_code = add_liked_song(username, song_data)
    return response, status_code
