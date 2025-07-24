import random      # 무작위 숫자를 만들어주는 라이브러리
import time        # 현재 시간과 날짜를 가져오는 라이브러리

# 🔧 DummySensor 클래스 정의: 화성 기지 환경 데이터를 임시로 생성하는 센서
class DummySensor:
    def __init__(self):
        # 다양한 환경 값을 저장할 딕셔너리
        self.env_values = {
            'mars_base_internal_temperature': None,       # 내부 온도 (°C)
            'mars_base_external_temperature': None,       # 외부 온도 (°C)
            'mars_base_internal_humidity': None,          # 내부 습도 (%)
            'mars_base_external_illuminance': None,       # 외부 광량 (W/m²)
            'mars_base_internal_co2': None,               # 내부 CO₂ 농도 (%)
            'mars_base_internal_oxygen': None             # 내부 O₂ 농도 (%)
        }

    # 🌡️ 센서 환경 값들을 무작위로 설정
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 1)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 1)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 1)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 1)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    # 📋 환경 값을 반환하고 로그 파일에 저장
    def get_env(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # 로그 텍스트 생성
        log_line = f'{timestamp}, ' \
                   f'{self.env_values["mars_base_internal_temperature"]}°C, ' \
                   f'{self.env_values["mars_base_external_temperature"]}°C, ' \
                   f'{self.env_values["mars_base_internal_humidity"]}%, ' \
                   f'{self.env_values["mars_base_external_illuminance"]}W/m², ' \
                   f'{self.env_values["mars_base_internal_co2"]}%, ' \
                   f'{self.env_values["mars_base_internal_oxygen"]}%\n'

        try:
            # 로그를 UTF-8-SIG 인코딩으로 저장 (문자 깨짐 방지)
            with open('mars_environment_log.txt', 'a', encoding='utf-8-sig') as file:
                file.write(log_line)
        except Exception as e:
            print('⚠️ 로그 저장 중 오류 발생:', e)

        return self.env_values

# 🌱 센서 사용 예시
ds = DummySensor()
ds.set_env()
env_data = ds.get_env()

# 결과 출력
for key, value in env_data.items():
    print(f'{key} = {value}')