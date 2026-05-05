import json
import os
from pathlib import Path

class SBFDetector:
    def __init__(self):
        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"
        self.file_path = self.app_path / "Logic1_analysis_result.json"
        self.result_file_path = self.app_path / "STD_status_result.json"
        self.data = []

    def load_logs(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                print(f"{self.file_path} 파일이 성공적으로 로드되었습니다.")
            else:
                print(f"{self.file_path} 파일이 존재하지 않습니다.")
        except Exception as e:
            print(f"파일 로드 중 에러 발생: {e}")

    def detect_bots(self):
        block_count = 0
        suspicious_count = 0

        if not self.data:
            print("분석할 데이터가 없음")
            return

        for res in self.data:
            std = res.get("std_deviation")
            count = res.get("connection_count")
            # Logic2에서 추가된 값


            if std is None or count is None:
                continue

            #  1. 데이터 부족
            if count < 5:
                res["status"] = "insufficient"

            #  2. 자동화 공격 (패턴 일정)
            elif std < 2:
                res["status"] = "block"
                print(f"IP : {res['ip']} 자동화 공격 (std: {std:.2f})")
                block_count += 1

            #  3. 애매 구간 → jitter.py 를써서 추가 분석 예정
            elif 2 <= std < 22:
                res["status"] = "suspicious"
                print(f"IP : {res['ip']} 애매 구간 (추가 분석 필요)")
                suspicious_count += 1


            #  4. 사람 / 랜덤 공격
            else:
                res["status"] = "normal"

        print(f"\n탐지 완료 : 탐지->{block_count}, 의심->{suspicious_count}")

    def save_results(self):
        try:
            with open(self.result_file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"분석 결과가 {self.result_file_path}에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 에러 발생: {e}")


if __name__ == "__main__":
    detector = SBFDetector()
    detector.load_logs()        
    detector.detect_bots()     
    detector.save_results()     
