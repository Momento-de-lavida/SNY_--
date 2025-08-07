import zipfile
import string
import itertools
import time
from multiprocessing import Process, Event, Value, cpu_count
from io import BytesIO

ZIP_PATH = 'emergency_storage_key.zip'
PW_FILE = 'password.txt'
CHARS = string.digits + string.ascii_lowercase
PW_LEN = 6

def try_password(zip_bytes, filename, pw):
    try:
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
            zf.read(filename, pwd=pw.encode())
        return True
    except Exception:
        return False

def worker(zip_bytes, filename, prefix_list, found, counter):
    for prefix in prefix_list:
        for tail in itertools.product(CHARS, repeat=PW_LEN-len(prefix)):
            if found.is_set():
                return
            pw = prefix + ''.join(tail)
            if try_password(zip_bytes, filename, pw):
                found.set()
                with open(PW_FILE, 'w') as f:
                    f.write(pw)
                print(f"\n[✔] 암호 찾음: {pw}")
                return
            # 이 부분에서 get_lock() 사용 가능!
            with counter.get_lock():
                counter.value += 1

def unlock_zip():
    with open(ZIP_PATH, 'rb') as f:
        zip_bytes = f.read()
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
        filename = zf.namelist()[0]  # 첫번째 파일명

    prefix_all = [''.join(p) for p in itertools.product(CHARS, repeat=2)]
    ncpu = cpu_count()
    chunk = len(prefix_all) // ncpu
    prefix_chunks = [prefix_all[i*chunk:(i+1)*chunk] for i in range(ncpu)]
    # 마지막 chunk에 남은 것도 포함
    if len(prefix_all) % ncpu != 0:
        prefix_chunks[-1].extend(prefix_all[ncpu*chunk:])

    # Manager().Event() 대신 Event()
    found = Event()
    counter = Value('i', 0)

    start = time.time()
    procs = [Process(target=worker, args=(zip_bytes, filename, chunk, found, counter)) for chunk in prefix_chunks]

    for p in procs: p.start()

    last = 0
    try:
        while not found.is_set() and any(p.is_alive() for p in procs):
            time.sleep(1)
            now = counter.value
            speed = now - last
            elapsed = int(time.time() - start)
            print(f"\r진행: {now:,}회 / {elapsed}s ({speed:,}/sec)", end='')
            last = now
    except KeyboardInterrupt:
        found.set()
    finally:
        for p in procs: p.terminate()
        for p in procs: p.join()
        print('\n모든 프로세스 종료.')

    # password.txt에 결과 남음
    try:
        with open(PW_FILE, 'r') as f:
            pw = f.read()
            print(f"[!] 최종 비밀번호: {pw}")
    except Exception:
        print("[!] 비밀번호를 찾지 못했습니다.")

if __name__ == '__main__':
    unlock_zip()
