#Jitter, CV 기준값 판단 프로그램 

import os,re,sys,time,json 
from pathlib import Path 

class Jitter_CV_detector:
    def __init__(self):
        self.jitter_content = None
        self.cv_content = None
        self.result = []
        self.JD=  []
        self.CVD = []

        #path 
        self.base_path = Path("/root/project/app")
        self.Jitter_CV_result_path = self.base_path / "Jitter_CV_result.json"
        self.Jitter_result_path = self.base_path / "Jitter_result.json"
        self.CV_result_path = self.base_path / "CV_result.json" 

    def Jitter_openfile(self):
        try:
            if os.path.exists(self.Jitter_result_path):
                print(f"{self.Jitter_result_path} 파일이 존재합니다.")
                with open(self.Jitter_result_path, "r", encoding = "utf-8") as f:
                    self.jitter_content=json.load(f)
                    print("파일 로드 성공\n")
            
            else:
                print(f"{self.Jitter_result_path} 파일이 존재하지 않습니다.")
                print("프로그램을 종료합니다.")
                sys.exit(1)


        except Exception as e:
            print(f"ERROR: {e}")

    def CV_openfile(self):
        try:
            if os.path.exists(self.CV_result_path):
                print(f"{self.CV_result_path} 파일이 존재합니다.")
                with open(self.CV_result_path, "r", encoding="utf-8") as f:
                    self.cv_content = json.load(f)
                    print("파일 로드 성공\n")

            else:
                print(f"{self.CV_result_path} 파일이 존재하지 않습니다.")
                print("프로그램을 종료합니다.")
                sys.exit(1)


        except Exception as e:
            print(f'ERROR: {e}')


    def Detector(self):
        try:
            for ip in self.jitter_content:
                jitter = self.jitter_content[ip]
                cv = self.cv_content[ip]

                print(f"\nIP: {ip}")
                print(f"Jitter: {jitter}")
                print(f"CV: {cv}")

                # 핵심 탐지
                if cv >= 0.35:

                    # 일반 slow brute
                    if 0.5 <= jitter < 16:
                        print("일반 슬로우 브루트포스 의심")

                        self.result.append({
                            "ip": ip,
                            "jitter": jitter,
                            "cv": cv,
                            "type": "normal_slow_bruteforce"
                        })

                    # 랜덤화 slow brute
                    elif 16<=jitter<=22:
                        print("랜덤화 슬로우 브루트포스 의심")

                        self.result.append({
                            "ip": ip,
                            "jitter": jitter,
                            "cv": cv,
                            "type": "randomized_slow_bruteforce"
                        })

                    else:   #CV값이 0.35이상이지만, Jitter 분석 시, 기준 값에 존재하지 않기 때문에 보다 정확한 검사가 필요함 
                        print("슬로우 브루트 포스 의심 -> 추가 분석을 진행해야 정확한 공격을 파악이 가능합니다.")   #JA3의 도입이 필요하다고 생각함

                        self.result.append({
                             "ip": ip,
                            "jitter": jitter,
                            "cv": cv,
                            "type": "unknown_slow_bruteforce"
                        })

                else:
                    print("정상 사용자 가능성 높음")

        except Exception as e:
            print(f"ERROR: {e}")

    
    def save_file(self):
        try:
            with open(self.Jitter_CV_result_path ,  "w", encoding = "utf-8" ) as f:
                json.dump(self.result, f, indent =  4, ensure_ascii = False) 
                print(f"{self.Jitter_CV_result_path} 파일 생성 완료")
            
        except Exception as e:
            print(f"ERROR: {e}")



if __name__=="__main__":
    D = Jitter_CV_detector()
    D.Jitter_openfile()
    D.CV_openfile()
    D.Detector()
    D.save_file()
