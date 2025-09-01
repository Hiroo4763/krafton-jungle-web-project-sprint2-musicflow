from flask import Blueprint, render_template, jsonify, session
from app.services.preference_service import *

preference_bp = Blueprint("preference", __name__)


# 선호 장르/아티스트 선택 페이지
@preference_bp.route("/preference")
def show_preference():
    user_id = session.get("user_id")
    if not user_id:
        return render_template("preference.html", status="need_login")
    return render_template("preference.html")


# 선호 장르/아티스트 저장 API
@preference_bp.route("/api/preference", methods=["POST"])
def api_preference():
    username = request.form.get("username")
    genres = request.form.getlist("genres[]")
    artists = request.form.getlist("artists[]")

    return insert_user_preference(username, genres, artists)
