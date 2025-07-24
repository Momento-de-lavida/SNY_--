import time        # 시간을 다룰 수 있는 도구 (예: 현재 시간, 대기 시간 등)
import json        # 데이터를 보기 좋게 출력할 수 있도록 변환해주는 도구
import random      # 무작위 숫자를 만들 때 사용하는 도구

# 센서 역할을 하는 DummySensor 클래스
class DummySensor:
    def __init__(self):
        # 센서가 측정할 환경 정보를 담는 딕셔너리 (상자 같은 거)
        self.env_values = {
            'mars_base_internal_temperature': None,       # 내부 온도 (°C)
            'mars_base_external_temperature': None,       # 외부 온도 (°C)
            'mars_base_internal_humidity': None,          # 내부 습도 (%)
            'mars_base_external_illuminance': None,       # 외부 빛 세기 (W/m²)
            'mars_base_internal_co2': None,               # 내부 이산화탄소 (%)
            'mars_base_internal_oxygen': None             # 내부 산소 (%)
        }

    # 센서 값들을 무작위로 설정하는 함수
    def set_env(self):
        # 각 항목에 정해진 범위 내에서 랜덤한 숫자를 넣음
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 1)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 1)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 1)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 1)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    # 📋 랜덤 값이 채워진 환경 정보를 반환하는 함수
    def get_env(self):
        self.set_env()               # 먼저 랜덤 환경값을 만들어 놓고
        return self.env_values       # 그 값을 반환해요

# MissionComputer 클래스: 센서 값을 받고 화면에 출력하는 역할
class MissionComputer:
    def __init__(self):
        # 초기 환경 정보 딕셔너리 설정 (처음엔 값이 0)
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

        self.ds = DummySensor()       # 센서 만들기
        self.env_history = []         # 5분 동안의 기록을 저장할 리스트
        self.start_time = time.time() # 시작 시간을 기억 (5분 평균용)

    # 센서 데이터를 받고 출력하는 함수
    def get_sensor_data(self):
        try:
            while True:  # 계속 반복 (5초마다)
                # 센서에서 환경 정보를 받아옴
                sensor_data = self.ds.get_env()

                # 받아온 센서 값을 저장소(env_values)에 복사
                self.env_values.update(sensor_data)

                # 화면에 보기 좋게 출력 (json 형식)
                print('📡 현재 센서 값:')
                print(json.dumps(self.env_values, indent=2))

                # 5분 평균을 위한 기록을 리스트에 저장
                self.env_history.append(sensor_data)

                # 시간이 300초(5분) 이상이면 평균을 계산
                if time.time() - self.start_time >= 300:
                    avg_values = {}
                    for key in self.env_values.keys():
                        # 각 항목별로 값을 모두 더한 뒤 갯수만큼 나눔
                        total = sum(entry[key] for entry in self.env_history)
                        avg_values[key] = round(total / len(self.env_history), 2)

                    # 5분 평균 값을 화면에 출력
                    print('🧮 5분 평균 값:')
                    print(json.dumps(avg_values, indent=2))

                    # 평균을 출력했으면 기록 초기화하고 시간도 새로 시작
                    self.env_history.clear()
                    self.start_time = time.time()

                # 5초 대기 후 다시 반복
                time.sleep(5)

        except KeyboardInterrupt:
            # 사람이 멈추고 싶을 때(Ctrl + C) 이 문구를 출력하고 종료
            print('🛑 System stopped….')

# MissionComputer를 만든 뒤 데이터를 받아보는 부분
RunComputer = MissionComputer()       # 클래스를 사용해서 컴퓨터를 만들기
RunComputer.get_sensor_data()         # 센서 값을 계속 출력