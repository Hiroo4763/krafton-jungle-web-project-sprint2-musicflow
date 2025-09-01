# auth 관련 라우트 정의
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
from app.services.auth_service import *


auth_bp = Blueprint("login", __name__)


# 로그인 페이지
@auth_bp.route("/login")
def show_login():
    user_id = session.get("user_id")
    if not user_id:
        return render_template("login.html")
    # 이미 로그인 상태면 안내 메시지 표시
    return render_template("login.html", status="already_login")


# 회원가입 페이지
@auth_bp.route("/register")
def show_register():
    return render_template("register.html")


# 아이디 찾기 페이지
@auth_bp.route("/findid")
def show_findid():
    return render_template("findid.html")


# 로그아웃 처리
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.show_login"))


# 아이디 찾기 결과 페이지
@auth_bp.route("/findid-reuslt")
def show_findid_result():
    return render_template("findid-result.html")


# 비밀번호 찾기 페이지
@auth_bp.route("/findpw")
def show_findpw():
    return render_template("findpw.html")


# 비밀번호 변경 페이지
@auth_bp.route("/changepw")
def show_changepw_page():
    user_id = session.get("user_id")
    if not user_id:
        # 로그인 필요 시 접근 제한
        return render_template("changepw.html", status="need_login")
    return render_template("changepw.html")


# 로그인 API
@auth_bp.route("/api/login", methods=["POST"])
def loginSystem():
    username = request.form.get("username")
    password = request.form.get("password")
    return process_login(username, password)


# 아이디 찾기 API
@auth_bp.route("/api/findid", methods=["POST"])
def findidSystem():
    name = request.form.get("name")
    birth = request.form.get("birth")
    return find_user_id(name, birth)


# 비밀번호 찾기 API
@auth_bp.route("/api/findpw", methods=["POST"])
def findpwSystem():
    global username2
    username2 = request.form.get("username")  # 이후 변경 단계에서 다시 사용됨
    name = request.form.get("name")
    birth = request.form.get("birth")
    return find_user_for_pw_change(username2, name, birth)


# 비밀번호 변경 API
@auth_bp.route("/api/changepw", methods=["POST"])
def changepwSystem():
    username = session.get("user_id")
    if not username:
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

    new_password = request.form.get("new_password")
    if not new_password and request.is_json:
        payload = request.get_json(silent=True) or {}
        new_password = payload.get("new_password")

    if not new_password:
        return jsonify({"success": False, "message": "새 비밀번호가 필요합니다."}), 400

    return change_user_password(username, new_password)


# 회원가입 API
@auth_bp.route("/api/register", methods=["POST"])
def registerSystem():
    username = request.form["username"]
    password = request.form["password"]
    nickname = request.form["nickname"]
    name = request.form["name"]
    birth = request.form["birth"]

    return save_user_info(username, password, nickname, name, birth)
