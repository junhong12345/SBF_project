#main_pipeline

import os,re,sys,time,json 
from pathlib import Path 

from Logic1 import LogAnalysis
from Logic2 import SBFDetector


class main_pipeline:
    def __init__(self):
        self.content = None
        self.result = None

        #path 
        self.total_path = Path("/root/project/app")
        self.logs_json_path = self.total_path / "logs.json"
        self.logic1_path = self.total_path / "Logic1.py"
        self.logic2_path = self.total_path / "Logic2.py"

    def main(self):
        try:
            #Logic1
            analysis = LogAnalysis()
            analysis.openfile()
            analysis.parsing()
            analysis.show_parsing_result()
            analysis.save_result()

            #Logic2
            detector = SBFDetector()
            detector.load_logs()        # 1. 로그 로드
            detector.detect_bots()      # 2. 봇 탐지
            detector.save_results()     # 3. 결과 저장

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ =="__main__":
    main = main_pipeline()
    main.main()