import zipfile  # ZIP 파일을 처리하기 위한 모듈
import string  # 문자열 관련 유틸리티 (숫자, 알파벳 등)
import itertools  # 반복 가능한 객체를 생성하는 유틸리티
import time  # 시간 측정 및 sleep 기능
from multiprocessing import Process, Event, Value, cpu_count  # 병렬 처리 관련 모듈
from io import BytesIO  # 메모리 기반 파일 객체

# ZIP 파일 경로 및 결과 저장 파일
ZIP_PATH = 'emergency_storage_key.zip'
PW_FILE = 'password.txt'

# 사용할 문자 집합: 숫자 + 소문자 알파벳
CHARS = string.digits + string.ascii_lowercase

# 비밀번호 길이 (고정)
PW_LEN = 6

# 주어진 비밀번호로 ZIP 파일을 열어보는 함수
def try_password(zip_bytes, filename, pw):
    try:
        # 메모리에서 ZIP 파일을 열고, 비밀번호로 파일을 읽어봄
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
            zf.read(filename, pwd=pw.encode())  # 비밀번호는 바이트로 인코딩
        return True  # 성공적으로 읽으면 비밀번호가 맞음
    except Exception:
        return False  # 실패하면 비밀번호가 틀림

# 각 프로세스에서 실행되는 작업 함수
def worker(zip_bytes, filename, prefix_list, found, counter):
    for prefix in prefix_list:  # 할당된 접두어 리스트 순회
        # 접두어를 제외한 나머지 자리수 조합 생성
        for tail in itertools.product(CHARS, repeat=PW_LEN-len(prefix)):
            if found.is_set():  # 다른 프로세스가 이미 비밀번호를 찾았으면 종료
                return
            pw = prefix + ''.join(tail)  # 전체 비밀번호 조합 생성
            if try_password(zip_bytes, filename, pw):  # 비밀번호 시도
                found.set()  # 찾았다는 이벤트 설정
                with open(PW_FILE, 'w') as f:  # 결과 파일에 저장
                    f.write(pw)
                print(f"\n[✔] 암호 찾음: {pw}")
                return
            # 시도 횟수 증가 (동기화된 공유 변수)
            with counter.get_lock():
                counter.value += 1

# ZIP 파일을 열고 비밀번호를 찾는 메인 함수
def unlock_zip():
    # ZIP 파일을 바이너리로 읽음
    with open(ZIP_PATH, 'rb') as f:
        zip_bytes = f.read()
    # ZIP 파일에서 첫 번째 파일 이름 추출
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
        filename = zf.namelist()[0]

    # 접두어 조합 생성 (2자리 조합: 총 36^2 = 1296개)
    prefix_all = [''.join(p) for p in itertools.product(CHARS, repeat=2)]

    # CPU 개수에 따라 접두어 리스트 분할
    ncpu = cpu_count()
    chunk = len(prefix_all) // ncpu
    prefix_chunks = [prefix_all[i*chunk:(i+1)*chunk] for i in range(ncpu)]

    # 나머지 접두어가 있다면 마지막 chunk에 추가
    if len(prefix_all) % ncpu != 0:
        prefix_chunks[-1].extend(prefix_all[ncpu*chunk:])

    # 비밀번호 찾음 여부를 공유하는 이벤트 객체
    found = Event()
    # 시도 횟수를 공유하는 변수
    counter = Value('i', 0)

    # 시작 시간 기록
    start = time.time()

    # 각 프로세스 생성 및 시작
    procs = [Process(target=worker, args=(zip_bytes, filename, chunk, found, counter)) for chunk in prefix_chunks]
    for p in procs:
        p.start()

    # 진행 상황 출력 루프
    last = 0
    try:
        while not found.is_set() and any(p.is_alive() for p in procs):
            time.sleep(1)  # 1초마다 업데이트
            now = counter.value  # 현재 시도 횟수
            speed = now - last  # 초당 시도 속도
            elapsed = int(time.time() - start)  # 경과 시간
            print(f"\r진행: {now:,}회 / {elapsed}s ({speed:,}/sec)", end='')
            last = now
    except KeyboardInterrupt:
        found.set()  # Ctrl+C로 중단 시 모든 프로세스 종료 요청
    finally:
        for p in procs:
            p.terminate()  # 프로세스 강제 종료
        for p in procs:
            p.join()  # 프로세스 종료 대기
        print('\n모든 프로세스 종료.')

    # 결과 파일에서 비밀번호 읽기
    try:
        with open(PW_FILE, 'r') as f:
            pw = f.read()
            print(f"[!] 최종 비밀번호: {pw}")
    except Exception:
        print("[!] 비밀번호를 찾지 못했습니다.")

# 프로그램 시작점
if __name__ == '__main__':
    unlock_zip()