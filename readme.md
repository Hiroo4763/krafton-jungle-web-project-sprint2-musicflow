# 웹개발 프로젝트 

## 📌 프로젝트 소개
이 프로젝트는 **사용자 맞춤 음악 추천과 커뮤니티 기능을 결합한 웹서비스**입니다.  
단순히 음악을 듣는 것에 그치지 않고, 좋아요한 곡을 기반으로 취향을 업데이트하고,  
다른 사용자들과 글·댓글로 소통할 수 있는 작은 음악 커뮤니티를 목표로 했습니다.  

크래프톤 정글 웹개발 캠프(12일 과정) 중 5일 동안(2025.08.16 ~ 2025.08.21),  
3명이 협업하여 **아이디어 기획 → 백엔드·프론트엔드 구현 → Docker 배포 → AWS EC2 배포**까지 전 과정을 경험했습니다.  

### 🌟 주요 특징
- Deezer API를 활용한 **실시간 음악 검색 및 추천**
- 사용자 **좋아요 기록 기반 취향 반영**
- 글쓰기·댓글·좋아요 기능을 갖춘 **커뮤니티 게시판**
- 개인 활동을 모아보는 **프로필 페이지** (작성 글 / 좋아요한 곡 조회)
- Docker와 AWS EC2를 활용한 **실제 서비스 환경 배포**

👉 **한 줄 요약**: *“음악을 중심으로 한 소셜 웹서비스 – 나만의 플레이리스트와 작은 커뮤니티를 동시에 경험할 수 있는 웹사이트”*

## 👥 팀원 소개
- 이동욱: 백엔드 (Flask, MongoDB, python, docker, 배포)
- 추용은: 백엔드 (Flask, MongoDB, DeezerAPI, python)
- 김태희: 프론트엔드 (HTML, CSS, JavaScript)

## 🚀 주요 기능
- 회원가입 / 로그인 / 아이디 찾기 / 비밀번호 찾기
- 커뮤니티
- 글쓰기, 댓글, 좋아요
- 음악 검색 및 추천 (Deezer API)
- 실시간 사용자 취향 업데이트 
- 프로필 관리 (좋아요한 음악, 작성한 글 조회)

## 🛠️ 기술 스택
- Backend: Flask, Python
- Frontend: HTML, CSS, JavaScript
- DB: MongoDB
- Deployment: Docker, AWS EC2

## 실행법
> python -m venv .venv

> call .venv/Scripts/activate             <---(CMD)

> pip install -r requirements.txt

### app/services/config.py에서 uri를 mongoDB 주소로 바꿔야 정상적인 실행 가능 

