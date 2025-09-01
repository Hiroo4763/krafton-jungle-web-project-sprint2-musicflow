import requests
from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta
from app.services.config import uri 

client = MongoClient(uri, 27017)
db = client["sprint2"]
posts_collection = db["posts"]


# Deezer 글로벌 차트 TOP10 조회
def get_popular_songs():
    try:
        url = "https://api.deezer.com/chart/0/tracks"
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json().get('data', [])
        
        songs = []
        for item in data[:10]:
            songs.append({
                'id': item.get('id'),
                'title': item.get('title_short'),
                'artist': item['artist'].get('name'),
                'album_art': item['album'].get('cover_medium'),
                'rank': item.get('rank'),
                'preview_url': item.get('preview')
            })
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Deezer API 요청 실패: {e}")
        return []
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}")
        return []


# 오늘 작성된 게시글 중 좋아요 TOP10 조회
def get_today_popular_posts():
    try:
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)

        pipeline = [
            {'$match': {'created_at': {'$gte': today_start, '$lt': tomorrow_start}}},
            {'$sort': {'likes': DESCENDING}},
            {'$limit': 10}
        ]
        
        popular_posts = list(posts_collection.aggregate(pipeline))
        
        for post in popular_posts:
            post['_id'] = str(post['_id'])
            
        return popular_posts
    except Exception as e:
        print(f"MongoDB 인기 게시글 조회 실패: {e}")
        return []