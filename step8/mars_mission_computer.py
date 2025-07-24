import platform   # 운영체제 정보를 가져오는 기본 모듈
import os         # CPU 정보, 메모리 확인용 기본 모듈
import time       # 시간 계산용
import json       # 보기 좋게 출력하는 도구

# MissionComputer 클래스 정의
class MissionComputer:
    def __init__(self):
        # 아무 데이터도 없지만 나중에 센서 정보가 들어올 수 있음
        self.env_values = {}

    # 시스템 기본 정보 확인
    def get_mission_computer_info(self):
        try:
            # 시스템 정보들을 딕셔너리로 정리
            info = {
                'Operating System': platform.system(),
                'OS Version': platform.version(),
                'CPU Type': platform.processor(),
                'CPU Core Count': os.cpu_count(),
                'Memory Size': self._get_memory_size()
            }

            print('🧾 미션 컴퓨터 시스템 정보:')
            print(json.dumps(info, indent=2))  # 보기 좋게 출력
        except Exception as e:
            print('⚠️ 시스템 정보 가져오기 오류:', e)

    # 컴퓨터의 부하 상태 확인
    def get_mission_computer_load(self):
        try:
            cpu_load = self._get_cpu_load()
            memory_load = self._get_memory_load()
            load = {
                'CPU Load (%)': cpu_load,
                'Memory Usage (%)': memory_load
            }
            filtered = self._filter_output(load)  # 필터링된 값 저장
            print('📈 미션 컴퓨터 실시간 부하:')
            print(json.dumps(filtered, indent=2))  # 필터링된 데이터 출력
        except Exception as e:
            print('⚠️ 시스템 부하 정보 가져오기 오류:', e)

            
        # setting.txt 파일을 읽고 출력 항목을 필터링하는 함수
    def _filter_output(self, data):
        try:
            with open('setting.txt', 'r', encoding='utf-8') as file:
                selected = json.loads(file.read())
            return {key: data[key] for key in selected if key in data}
        except Exception as e:
            print('⚠️ setting.txt 읽기 오류:', e)
            return data # 설정 파일 없거나 오류가 생기면 전체 출력   
     

    # 메모리 크기 계산 (단위: MB)
    def _get_memory_size(self):
        try:
            if os.name == 'nt':  # Windows일 경우
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
            else:  # Unix/Linux
                if hasattr(os, 'sysconf'):
                    if 'SC_PAGE_SIZE' in os.sysconf_names and 'SC_PHYS_PAGES' in os.sysconf_names:
                        page_size = os.sysconf('SC_PAGE_SIZE')
                        phys_pages = os.sysconf('SC_PHYS_PAGES')
                        return round((page_size * phys_pages) / (1024 * 1024), 2)
            return 'N/A'
        except Exception as e:
            print('⚠️ 메모리 크기 가져오기 오류:', e)
            return 'N/A'


    # CPU 사용률 계산 (0~100%)
    def _get_cpu_load(self):
        # 아주 간단한 계산: 사용률은 측정되지 않으면 0으로 처리
        if os.name == 'posix':
            return round(os.getloadavg()[0] * 100 / os.cpu_count(), 2)
        return 0.0  # Windows에서는 getloadavg 사용 불가

    # 메모리 사용률 계산 (Linux/Unix 기준)
    def _get_memory_load(self):
        try:
            if os.name == 'nt':  # Windows 환경일 경우
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

                mem = MEMORYSTATUSEX()
                mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))

                used = mem.ullTotalPhys - mem.ullAvailPhys
                percent_used = used / mem.ullTotalPhys * 100
                return round(percent_used, 2)

            else:  # Unix/Linux
                with open('/proc/meminfo', 'r') as file:
                    lines = file.readlines()
                    mem_total = 0
                    mem_available = 0
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

# 미션 컴퓨터를 실행해보는 코드
runComputer = MissionComputer()
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()

def create_default_setting_file():
    with open('setting.txt', 'w', encoding='utf-8') as file:
        file.write('["CPU Load (%)", "Memory Usage (%)"]')

create_default_setting_file()  # setting.txt 파일이 없으면 생성