from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


BASE_DIR = Path(__file__).resolve().parent



def save_log(data):
    now_time = datetime.now()
    formatted = now_time.strftime("%Y-%m-%d_%H")  # 시간 단위
    log_file = BASE_DIR / f"{formatted}_logs.json"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


@app.get("/")
def root():
    return "OK"
@app.get("/health_check")
def health_check():
    return "Fast_API Service OK"


@app.get("/login")
def get_login():
    return "Please requests to POST"

@app.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    ip = request.client.host

    log = {
        "timestamp": time.time(),   #현재 시간
        "ip": ip,   #ip
        "username": data.get("username"),   #시도한 아이디
        "password": data.get("password"),   #시도한 비번
        "result": "fail",   #로그인 시도 실패 , 성공(허니팟이면 무조건 실패여서 fail 고정)
        "user_agent": request.headers.get("user-agent"),    #user_agent
        "language": request.headers.get("accept-language"),# 사용자 언어 설정
        "screen": data.get("screen"),   #화면 해상도
        "timezone": data.get("timezone")       #사용자 시간대
    }

    save_log(log)

    return {"status": "ok"}














