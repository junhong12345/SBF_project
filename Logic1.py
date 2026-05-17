import os
import sys
import json
from pathlib import Path
import numpy as np

class LogAnalysis:
    def __init__(self):
        self.content = None
        self.result = None

        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"
        self.file_path = self.app_path / "logs.json"

        self.ip_dict = {}

    def openfile(self):
        try:
            if os.path.isfile(self.file_path) and os.path.exists(self.file_path):
                print(f"{self.file_path} 파일이 존재합니다.")
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.content = f.read()
            else:
                print(f"{self.file_path} 파일이 존재하지 않습니다.")
                sys.exit(1)
        except Exception as e:
            print(f'ERROR: {e}')

    def parsing(self):
        try:
            if not self.content:
                print("파일이 비어있습니다.")
                sys.exit(1)

            lines = self.content.split('\n')

            for line in lines:
                if not line.strip():
                    continue

                log_data = json.loads(line)
                ip = log_data.get("ip")
                timestamp = log_data.get("timestamp")
                username = log_data.get("username")

                if ip and timestamp:
                    if ip not in self.ip_dict:
                        self.ip_dict[ip] = {
                            "username": username,
                            "timestamps": []
                        }
                        print(f"새로운 접속 아이피 감지: {ip} (사용자명: {username})")

                    self.ip_dict[ip]["timestamps"].append(timestamp)

            print(f"파싱 완료: {len(self.ip_dict)}개의 IP 감지")

        except Exception as e:
            print(f'Parsing ERROR: {e}')

    def show_parsing_result(self):
        print("\n" + "="*40)
        print("IP별 접속 기록 요약")
        print("="*40)

        for ip, data in self.ip_dict.items():
            timestamps = sorted(data["timestamps"])  # 문제2: 정렬 추가

            print(f"IP: {ip}")
            print(f"사용자명: {data['username']}")
            print(f"접속 횟수: {len(timestamps)}")
            print(f"타임스탬프 (전체): {timestamps}")  # 문제3: 전체 출력
            print("-"*40)

    def intervals(self, timestamps):    #REQ-007
        if len(timestamps) < 2:
            return []

        intervals = []
        for i in range(1, len(timestamps)):
            diff = timestamps[i] - timestamps[i-1]
            intervals.append(diff)

        return intervals

    def get_std(self, intervals):   #REQ-008
        if not intervals:
            return 0.0
        return np.std(intervals)

    def save_result(self):
        try:
            result_list = []

            for ip, data in self.ip_dict.items():
                timestamps = sorted(data["timestamps"])  # 정렬 필수
                intervals = self.intervals(timestamps)
                std_value = self.get_std(intervals)

                res_obj = {
                    "ip": ip,
                    "username": data["username"],
                    "connection_count": len(timestamps),
                    "std_deviation": std_value,
                    "status": "allow"
                }

                result_list.append(res_obj)

            save_path = self.app_path / "Logic1_analysis_result.json"

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(result_list, f, ensure_ascii=False, indent=4)

            print(f"분석 결과 저장 완료 → {save_path}")

        except Exception as e:
            print(f"결과 저장 오류: {e}")

if __name__ == "__main__":
    analysis = LogAnalysis()
    analysis.openfile()
    analysis.parsing()
    analysis.show_parsing_result()
    analysis.save_result()
