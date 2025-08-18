import os
import datetime
import sounddevice as sd
import soundfile as sf

class JarvisRecorder:
    def __init__(self, folder='records'):
        self.folder = folder
        # records 폴더가 존재하지 않으면 생성
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def record_voice(self, duration=10, samplerate=44100):
        """주어진 시간(duration) 동안 음성 녹음 후 파일로 저장"""
        print(f'녹음을 시작합니다. {duration}초 동안 녹음됩니다...')
        # 녹음 시작
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # 녹음 종료까지 대기

        # 파일 이름 생성: 년월일-시분초.wav
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = os.path.join(self.folder, f'{timestamp}.wav')

        # 녹음 데이터 파일로 저장
        sf.write(filename, recording, samplerate)
        print(f'녹음이 완료되어 {filename}에 저장되었습니다.')
        return filename

    def list_records(self, start_date=None, end_date=None):
        """폴더 내 녹음 파일 리스트 출력, 필요시 날짜 범위 필터링"""
        files = sorted(os.listdir(self.folder))
        filtered = []
        for f in files:
            if f.endswith('.wav'):
                if start_date or end_date:
                    # 파일명에서 날짜 추출
                    file_date = datetime.datetime.strptime(f[:8], '%Y%m%d').date()
                    if start_date and file_date < start_date:
                        continue
                    if end_date and file_date > end_date:
                        continue
                filtered.append(f)
        return filtered

# 실행 예제
if __name__ == '__main__':
    jarvis = JarvisRecorder()
    # 5초 동안 녹음
    jarvis.record_voice(duration=5)
    # 녹음 파일 목록 출력
    print(jarvis.list_records())
