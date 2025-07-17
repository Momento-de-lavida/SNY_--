# 전역 변수 선언
material = ''
diameter = 0.0
thickness = 1.0
area = 0.0
weight = 0.0

import math

# 반구체 면적 및 무게 계산 함수
def sphere_area(diameter_input='', material_input='유리', thickness_input=1.0):
    global material, diameter, thickness, area, weight

    # 기본 지름 적용 (입력하지 않거나 공백이면)
    if not diameter_input:
        diameter_input = 0.10  # 단위: m (10cm = 0.10m)

    try:
        diameter = float(diameter_input)
        thickness = float(thickness_input)

        if diameter <= 0 or thickness <= 0:
            print('지름과 두께는 0보다 커야 해요!')
            return

    except ValueError:
        print('숫자를 올바르게 입력해 주세요!')
        return

    # 재질 밀도 (g/cm³)
    densities = {
        '유리': 2.4,
        '알루미늄': 2.7,
        '탄소강': 7.85
    }

    if material_input not in densities:
        print('지원되지 않는 재질입니다. 유리, 알루미늄, 탄소강 중 하나를 입력하세요.')
        return

    material = material_input

    # 면적 계산: 반구체 전체 면적 (m²)
    radius = diameter / 2
    area = round(3 * math.pi * (radius ** 2), 4)

    # 면적 cm²로 변환
    area_cm2 = area * 10000

    # 무게 계산
    weight_g = area_cm2 * thickness * densities[material]
    weight = round((weight_g / 1000) * 0.38, 3)  # 화성 중력 적용

    # 결과 출력
    print(f'\n🛠️ 계산 결과:')
    print(f'재질     : {material}')
    print(f'지름     : {diameter:.2f}m')
    print(f'두께     : {thickness:.2f}cm')
    print(f'전체 면적: {area}㎡')
    print(f'화성 무게: {weight}kg\n')

# 반복 실행 루프
while True:
    d = input('지름을 입력하세요 (m, 기본값: 0.10m) [종료하려면 "exit"]: ').strip()
    if d.lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    m = input('재질을 입력하세요 (유리, 알루미늄, 탄소강) [종료하려면 "exit"]: ').strip()
    if m.lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    t = input('두께를 입력하세요 (cm, 기본값: 1.0) [종료하려면 "exit"]: ').strip()
    if t.lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    # 함수 호출
    sphere_area(d if d else '', m if m else '유리', t if t else 1.0)