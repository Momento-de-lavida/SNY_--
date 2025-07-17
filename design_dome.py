import numpy as np

# CSV 파일에서 숫자 데이터 읽기
arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', skip_header=1, usecols=1)
arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', skip_header=1, usecols=1)
arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', skip_header=1, usecols=1)

# 배열 합치기
parts = np.concatenate((arr1, arr2, arr3))

# 평균값 구하기
average_strength = np.mean(parts)

# 평균보다 낮은 부품 강도 필터링
low_strength_parts = parts[parts < 50]

# 저장하기 (예외처리 포함)
try:
    np.savetxt('parts_to_work_on.csv', low_strength_parts, delimiter=',')
except Exception as e:
    print('파일 저장 중 문제가 생겼어요:', e)
    

# 보너스 과제

try:
    # CSV 파일 읽기
    parts2 = np.genfromtxt('parts_to_work_on.csv', delimiter=',')

    # 전치 행렬 만들기 (1행으로 펼치기)
    parts2 = np.genfromtxt('parts_to_work_on.csv', delimiter=',')
    parts2 = parts2.reshape(-1, 1)  # 1열로 바꾸기
    parts3 = parts2.T               # transpose 사용
    

    # 출력
    print('\n전체 평균 강도:', average_strength)
    print('\n보강이 필요한 부품 강도 목록:')
    print(low_strength_parts)

    print('\n전치 행렬 결과:')
    print(parts3)

except Exception as e:
    print('보너스 과제 처리 중 오류가 발생했어요:', e)