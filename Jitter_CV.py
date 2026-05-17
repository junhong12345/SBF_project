import os,re,sys,time,json
from pathlib import Path

class Jitter:
    def __init__(self):
        self.content = None
        self.result = None

        # 결과 저장 딕셔너리
        self.jitter_data = {}
        self.cv_data = {}

        # path
        self.base_path = Path("/root/project/app")

        # Logic2 결과 파일
        self.STD_filtered_result_path = self.base_path / "STD_filtered_result.json"

        # 로그 파일
        self.logs_json_path = self.base_path / "logs.json"

        # 결과 저장 파일
        self.Jitter_result_path = self.base_path / "Jitter_result.json"
        self.CV_result_path = self.base_path / "CV_result.json"


    def openfile(self):
        try:
            if os.path.isfile(self.STD_filtered_result_path):
                print("STD_filtered_result 파일이 존재합니다")
                with open(self.STD_filtered_result_path, "r", encoding="utf-8") as analysis_file:
                    self.data = json.load(analysis_file)

                print("파일 로드 완료")

            else:
                print("STD_filtered_result 파일이 존재하지 않습니다.")
                sys.exit(1)

        except Exception as e:
            print(f"ERROR: {e}")


    def analysis_file(self):
        try:
            self.ip = []
            self.interval_data = {}
            self.std_data = {}

            # Logic2 결과 로드
            for result in self.data:
                ip = result.get("ip", "unknown")
                std = result.get("std_deviation", 0)

                self.ip.append(ip)
                self.std_data[ip] = std

            # logs.json 확인
            if self.ip:
                if os.path.isfile(self.logs_json_path):
                    print("logs_json 파일이 존재합니다")
                    with open(self.logs_json_path, "r", encoding="utf-8") as logs_file:
                        self.logs_data = logs_file.read()
                    print("logs.json 파일 로드 완료")
                else:
                    print("logs.json 파일이 존재하지 않습니다")
                    return

            else:
                print("추가 분석 대상 IP가 존재하지 않습니다")
                return

            # timestamp 저장
            self.ip_timestamp = {}
            timestamp_line = self.logs_data.splitlines()

            for line in timestamp_line:
                log = json.loads(line)
                log_ip = log.get("ip")
                timestamp = float(log.get("timestamp"))

                if log_ip in self.ip:
                    if log_ip not in self.ip_timestamp:
                        self.ip_timestamp[log_ip] = []
                    self.ip_timestamp[log_ip].append(timestamp)

            print(self.ip_timestamp)


            # IP별 분석
            for ip in self.ip_timestamp:
                timestamps = self.ip_timestamp[ip]
                timestamps.sort()

                # interval 계산
                interval_list = []
                for i in range(1, len(timestamps)):
                    interval = timestamps[i] - timestamps[i - 1]
                    interval_list.append(interval)
                self.interval_data[ip] = interval_list

                # jitter 계산
                interval_change_list = []
                for i in range(1, len(interval_list)):
                    interval_change = abs(interval_list[i] - interval_list[i - 1])
                    interval_change_list.append(interval_change)

                # jitter 평균 계산
                if len(interval_change_list) > 0:
                    total = 0

                    for change in interval_change_list:
                        total += change

                    self.jitter_data[ip] = total / len(interval_change_list)
                else:
                    self.jitter_data[ip] = 0

                print(f"\nIP: {ip}")
                print(f"Jitter: {self.jitter_data[ip]}")

        except Exception as e:
            print(f"ERROR: {e}")


    def cv_analysis_file(self):
        try:
            for ip in self.interval_data:
                interval_list = self.interval_data[ip]
                if len(interval_list) == 0:
                    print(f"{ip} interval 데이터가 존재하지 않음")
                    continue

                # interval 평균
                mean = sum(interval_list) / len(interval_list)
                # Logic1 std 값
                std = self.std_data[ip]

                # CV 계산
                if mean != 0:
                    self.cv_data[ip] = std / mean

                else:
                    self.cv_data[ip] = 0


                print(f"\nIP: {ip}")
                print(f"평균 interval: {mean}")
                print(f"표준편차: {std}")
                print(f"CV: {self.cv_data[ip]}")


        except Exception as e:
            print(f"ERROR: {e}")


    def save_file(self):
        try:
            # Jitter 저장
            if self.jitter_data:
                print("Jitter 계산 값 저장 시작")
                with open(self.Jitter_result_path, "w", encoding="utf-8") as f:
                    json.dump(
                        self.jitter_data,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                print(f"{self.Jitter_result_path} 저장 완료")

            else:
                print("Jitter 계산 값이 존재하지 않습니다.")
                sys.exit(1)

            # CV 저장
            if self.cv_data:
                print("CV 계산 값 저장 시작")
                with open(self.CV_result_path, "w", encoding="utf-8") as f:
                    json.dump(
                        self.cv_data,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                print(f"{self.CV_result_path} 저장 완료")

            else:
                print("CV 계산 값이 존재하지 않습니다.")
                sys.exit(1)

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    jitter_detector = Jitter()
    jitter_detector.openfile()
    jitter_detector.analysis_file()
    jitter_detector.cv_analysis_file()
    jitter_detector.save_file()
