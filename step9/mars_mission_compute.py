
#1.필요한 도구 불러오기(기초 라이브러리 import)
import platform       # 운영체제 정보 확인용
import os             # CPU 및 메모리 관련 정보 확인용
import time           # 주기적인 실행을 위한 시간 관리
import json           # 출력 결과를 보기 좋게 정리하기 위한 JSON 출력
import threading      # 멀티 쓰레드 실행용 (표준 라이브러리 허용됨)
import multiprocessing  # 멀티 프로세스 실행용 (표준 라이브러리 허용됨)

#2.미션 컴퓨터 클래스 정의(컴퓨터 상태 확인용 도우미)
class MissionComputer:
    def __init__(self):
        self.env_values = {}  # 센서 데이터가 들어올 수 있는 공간 (추후 확장)

    #3.시스템 정보 출력
    def get_mission_computer_info(self):
        try:
            info = {
                'Operating System': platform.system(), # 운영체제 이름
                'OS Version': platform.version(), # 운영체제의 세부 버전
                'CPU Type': platform.processor(), # CPU 종류
                'CPU Core Count': os.cpu_count(), # CPU 코어 개수
                'Memory Size': self._get_memory_size() # 물리 메모리 전체 크기
            }
            filtered = self._filter_output(info)  # setting.txt 적용하여 필요한 항목만 보여주기
            print('🧾 미션 컴퓨터 시스템 정보:')
            print(json.dumps(info, indent=2)) # 보기 좋게 JSON 형태로 출력

        except Exception as e:
            print('⚠️ 시스템 정보 가져오기 오류:', e)

    #4.시스템 부하(성능 상태) 출력
    def get_mission_computer_load(self):
        try:
            cpu_load = self._get_cpu_load() # CPU 사용률 확인

            memory_load = self._get_memory_load() # 메모리 사용률 확인

            load = {
                'CPU Load (%)': cpu_load, # CPU 사용 비율

                'Memory Usage (%)': memory_load # 메모리 사용 비율

            }
            filtered = self._filter_output(load)  # setting.txt 파일 기준 필터링
            print('📈 미션 컴퓨터 실시간 부하:')
            print(json.dumps(filtered, indent=2))  # 보기 좋게 출력

        except Exception as e:
            print('⚠️ 시스템 부하 정보 가져오기 오류:', e)

    #5.센서 데이터 출력 예시 (가상의 값)
    def get_sensor_data(self):
        try:
            sensor = {
                'Temperature': 22.8, # 임의의 온도 값
                'Humidity': 43.5,  # 임의의 습도 값
                'Radiation': 0.02 # 임의의 방사능 값

            }
            filtered = self._filter_output(sensor)  # 필터 적용
            print('📟 미션 센서 정보:')
            print(json.dumps(filtered, indent=2))
        except Exception as e:
            print('⚠️ 센서 정보 가져오기 오류:', e)

    #6. 주기적으로 모니터링하는 함수들 (20초 간격)
    def monitor_info(self):
        while True:
            self.get_mission_computer_info() # 시스템 정보 출력 반복
            time.sleep(20)   # 20초 대기 후 다시 실행

    def monitor_load(self):
        while True:
            self.get_mission_computer_load() # 시스템 부하 출력 반복

            time.sleep(20)

    def monitor_sensor(self):
        while True:
            self.get_sensor_data()  # 센서 데이터 출력 반복

            time.sleep(20)

    #7. 출력 항목 필터링 함수(setting.txt를 읽고 출력 항목 필터링)
    def _filter_output(self, data):
        try:
            with open('setting.txt', 'r', encoding='utf-8') as file:
                selected = json.loads(file.read()) # setting.txt 파일에서 필터 항목 읽기

            return {key: data[key] for key in selected if key in data} # 필요한 항목만 추림
        except Exception as e:
            print('⚠️ setting.txt 읽기 오류:', e)
            return data  # 설정 파일 없으면 전체 다 출력

    #8. 물리 메모리 크기 계산 (단위: MB)
    def _get_memory_size(self):
        try:
            if os.name == 'nt':  # Windows

                import ctypes

                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]

                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

                total_mb = stat.ullTotalPhys / (1024 * 1024)
                return round(total_mb, 2)
            
              # ctypes 사용해 물리 메모리 정보 구조체 정의 및 추출

            else: # Linux/Unix
 
                if hasattr(os, 'sysconf'):
                    page_size = os.sysconf('SC_PAGE_SIZE')
                    phys_pages = os.sysconf('SC_PHYS_PAGES')
                    return round((page_size * phys_pages) / (1024 * 1024), 2)
                  # os.sysconf로 페이지 사이즈와 총 페이지 수로 계산
            return 'N/A'
        except Exception as e:
            print('⚠️ 메모리 크기 가져오기 오류:', e)
            return 'N/A'

    #9. CPU 사용률과 메모리 사용률 계산 (단순 방법)
    def _get_cpu_load(self):  # 현재 시스템이 POSIX(Linux나 Mac)인지 확인
        if os.name == 'posix':
             # getloadavg()[0]: 최근 1분 동안의 평균 CPU 부하 계산
             # os.cpu_count(): CPU 코어 수
             # 계산된 평균 부하를 CPU 개수 기준으로 비율로 환산 후 소수점 2자리 반올림

            return round(os.getloadavg()[0] * 100 / os.cpu_count(), 2)
           
        return 0.0    # Windows는 간단히 0으로 설정

    def _get_memory_load(self):
        try:
               # 시스템이 Windows인 경우

            if os.name == 'nt':
                import ctypes # Windows 시스템 API 호출을 위한 모듈

        # 메모리 상태 구조 정의

                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),# 전체 물리 메모리

                        ('ullAvailPhys', ctypes.c_ulonglong), # 사용 가능한 물리 메모리

                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]

                mem = MEMORYSTATUSEX()
                mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                 # 시스템 호출로 메모리 정보 채우기

                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))

                # 사용된 메모리 계산: 전체 - 사용 가능

                used = mem.ullTotalPhys - mem.ullAvailPhys
                percent_used = used / mem.ullTotalPhys * 100
                return round(percent_used, 2)
            else:
                # Linux/Unix 시스템인 경우

                with open('/proc/meminfo', 'r') as file:
                    lines = file.readlines()
                    mem_total = 0 # 전체 메모리

                    mem_available = 0 # 사용 가능한 메모리
              
                  # 각 줄에서 원하는 정보 추출
                    for line in lines:
                        if 'MemTotal:' in line:
                            mem_total = int(line.split()[1])
                        elif 'MemAvailable:' in line:
                            mem_available = int(line.split()[1])
                    if mem_total == 0:
                        return 0.0
                    used = mem_total - mem_available
                    return round(used / mem_total * 100, 2)
        except Exception as e:
            print('⚠️ 메모리 사용량 가져오기 오류:', e)
            return 0.0

#10.setting.txt 기본 생성 함수
def create_default_setting_file(): # 설정 파일을 UTF-8로 새로 만들고 기본 항목을 넣어줌

    with open('setting.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps([
            "Operating System", "OS Version", "CPU Type", "CPU Core Count", "Memory Size",
            "CPU Load (%)", "Memory Usage (%)", "Temperature"
        ]))

# 실행용 메인 코드(멀티 쓰레드&사용자 입력)
if __name__ == '__main__':
    create_default_setting_file()  # 설정 파일 생성

     # 미션 컴퓨터 인스턴스 생성
    runComputer = MissionComputer()
    # 각 기능을 쓰레드로 실행 → 동시에 모니터링
    thread1 = threading.Thread(target=runComputer.monitor_info) # 시스템 정보

    thread2 = threading.Thread(target=runComputer.monitor_load) # CPU/메모리 부하

    thread3 = threading.Thread(target=runComputer.monitor_sensor)# 센서 데이터

    # 쓰레드 시작
    thread1.start()
    thread2.start()
    thread3.start()

    # 보너스: 키 입력 시 종료
    try:
        while True:
            cmd = input('종료하려면 q 입력: ')
            if cmd == 'q':
                print('🔚 모니터링 중단됨')
                break
    except KeyboardInterrupt: # 사용자가 Ctrl + C 눌렀을 경우
        print('🔌 사용자 중단')

    # 프로세스 실행 예시 (멀티 시스템 시나리오)
    # runComputer1 = MissionComputer()
    # runComputer2 = MissionComputer()
    # runComputer3 = MissionComputer()

    # p1 = multiprocessing.Process(target=runComputer1.monitor_info)
    # p2 = multiprocessing.Process(target=runComputer2.monitor_load)
    # p3 = multiprocessing.Process(target=runComputer3.monitor_sensor)

    # p1.start()
    # p2.start()
    # p3.start()