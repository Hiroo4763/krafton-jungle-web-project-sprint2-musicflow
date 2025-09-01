from flask import jsonify
from pymongo import MongoClient
from app.services.config import uri
from collections import Counter
from datetime import datetime

client = MongoClient(uri, 27017)
db = client["sprint2"]
users_collection = db["users"]
posts_collection = db["posts"]


# 사용자 프로필 조회
def get_user_profile(username):
    try:
        user_data = users_collection.find_one(
            {"username": username}, {"password": 0, "_id": 0}
        )
        if not user_data:
            return jsonify({"success": False, "message": "사용자 정보를 찾을 수 없습니다."}), 404

        user_posts = list(posts_collection.find({"username": username}))
        for post in user_posts:
            post["_id"] = str(post["_id"])

        profile_data = {
            "userInfo": {
                "name": user_data.get("name"),
                "nickname": user_data.get("nickname"),
                "birth": user_data.get("birth"),
            },
            "likedSongs": user_data.get("like_music", []),
            "authoredPosts": user_posts,
        }

        return jsonify({"success": True, "data": profile_data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "프로필 조회 오류", "error": str(e)}), 500


# 좋아요 곡 추가 + 아티스트 선호 업데이트
def add_liked_song(username, song_data):
    try:
        # 이미 좋아요한 곡인지 확인
        user = users_collection.find_one(
            {"username": username, "like_music.track_id": song_data.get("track_id")}
        )
        if user:
            return jsonify({"success": False, "message": "이미 좋아요한 노래입니다."}), 409

        new_song = {
            "track_id": song_data.get("track_id"),
            "title": song_data.get("title"),
            "artist_name": song_data.get("artist"),
            "album_cover": song_data.get("album_cover"),
            "preview": song_data.get("preview"),
        }

        result = users_collection.update_one(
            {"username": username}, {"$push": {"like_music": new_song}}
        )
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "사용자를 찾을 수 없습니다."}), 404

        # 아티스트 선호 업데이트 (3회 이상 좋아요시)
        user = users_collection.find_one({"username": username})
        liked_songs = user.get("like_music", [])
        artist_counts = Counter([song["artist_name"] for song in liked_songs])
        preferred_artists = [artist for artist, count in artist_counts.items() if count >= 3]

        users_collection.update_one(
            {"username": username},
            {"$addToSet": {"artists": {"$each": preferred_artists}}},
        )

        return jsonify({"success": True, "message": "좋아요 목록에 추가되었습니다."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "좋아요 처리 오류", "error": str(e)}), 500


# 좋아요 곡 취소
def remove_liked_song(username, track_id):
    try:
        try:
            track_id_as_int = int(track_id)
            query = {"$or": [{"track_id": track_id_as_int}, {"track_id": track_id}]}
        except (ValueError, TypeError):
            query = {"track_id": track_id}

        result = users_collection.update_one(
            {"username": username}, {"$pull": {"like_music": query}}
        )
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "사용자를 찾을 수 없습니다."}), 404
        if result.modified_count == 0:
            return jsonify({"success": False, "message": "해당 곡을 찾을 수 없습니다."}), 404

        return jsonify({"success": True, "message": "좋아요가 취소되었습니다."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "좋아요 취소 오류", "error": str(e)}), 500


# 이름 변경
def db_change_name(username, new_name):
    try:
        result = users_collection.update_one(
            {"username": username}, {"$set": {"name": new_name}}
        )
        return result.modified_count == 1
    except Exception:
        return False


# 닉네임 변경
def db_change_nickname(username, new_nickname):
    try:
        result = users_collection.update_one(
            {"username": username}, {"$set": {"nickname": new_nickname}}
        )
        return result.modified_count == 1
    except Exception:
        return False


# 생년월일 변경
def db_change_birth(username, new_birth_str):
    try:
        # YYYY-MM-DD 형식 검증
        datetime.strptime(new_birth_str, "%Y-%m-%d")
        result = users_collection.update_one(
            {"username": username}, {"$set": {"birth": new_birth_str}}
        )
        return result.modified_count == 1
    except Exception:
        return False
