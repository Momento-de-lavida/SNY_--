# 전역 변수 선언
material = ''
diameter = 0.0
thickness = 1.0
area = 0.0
weight = 0.0

def sphere_area(diameter_input, material_input='유리', thickness_input=1.0):
    global material, diameter, thickness, area, weight

    try:
        diameter = float(diameter_input)
        if diameter <= 0:
            print('지름은 0보다 커야 해요!')
            return

        thickness = float(thickness_input)
    except ValueError:
        print('숫자를 올바르게 입력해 주세요!')
        return

    # 반지름 계산
    radius = diameter / 2

    # 반구 면적 계산
    pi = 3.14159265359
    area = round(2 * pi * (radius ** 2), 3)

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

    # 면적 cm²로 변환 (m² → cm²)
    area_cm2 = area * 10000

    # 무게 계산 (g)
    weight_g = area_cm2 * thickness * densities[material]

    # 화성 중력 적용 (kg 단위로 변환)
    weight = round((weight_g / 1000) * 0.38, 3)

    # 결과 출력
    print(f'재질 =⇒ {material}, 지름 =⇒ {diameter}m, 두께 =⇒ {thickness}cm, 면적 =⇒ {area}m², 무게 =⇒ {weight}kg')

# 반복 실행
while True:
    d = input('지름을 입력하세요 (m) [종료하려면 "exit" 입력]: ')
    if d.strip().lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    # 지름이 숫자인지 확인
    try:
        float(d)
    except ValueError:
        print('지름은 숫자여야 해요!')
        continue

    m = input('재질을 입력하세요 (유리, 알루미늄, 탄소강): ')
    if m.strip().lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    t = input('두께를 입력하세요 (cm, 기본 1): ')
    if t.strip().lower() == 'exit':
        print('프로그램을 종료합니다.')
        break

    # 두께가 숫자인지 확인
    try:
        float(t if t else 1.0)
    except ValueError:
        print('두께는 숫자여야 해요!')
        continue

    sphere_area(d, m if m else '유리', t if t else 1.0)