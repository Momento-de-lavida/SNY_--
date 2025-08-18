import os
import datetime
import csv
import tkinter as tk
from tkinter import scrolledtext, messagebox
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# 녹음, STT, 키워드 검색 통합 클래스
class JavisApp:
    def __init__(self):
        self.records_dir = 'records'
        os.makedirs(self.records_dir, exist_ok=True)

        # GUI 초기화
        self.root = tk.Tk()
        self.root.title('Javis Voice Recorder & Search')

        # 녹음 버튼
        self.record_btn = tk.Button(self.root, text='녹음 시작', command=self.record_audio)
        self.record_btn.pack(pady=5)

        # 키워드 입력
        tk.Label(self.root, text='검색 키워드:').pack()
        self.keyword_entry = tk.Entry(self.root)
        self.keyword_entry.pack(pady=5)

        # 검색 버튼
        self.search_btn = tk.Button(self.root, text='검색', command=self.search_keyword)
        self.search_btn.pack(pady=5)

        # 결과 출력
        self.result_box = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.result_box.pack(pady=5)

    def record_audio(self, duration=5):
        """마이크로 음성 녹음 후 wav 저장"""
        fs = 44100
        messagebox.showinfo('녹음', f'{duration}초간 녹음 시작합니다.')
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        filename_wav = os.path.join(self.records_dir, f'{timestamp}.wav')
        sf.write(filename_wav, recording, fs)
        messagebox.showinfo('녹음 완료', f'녹음 파일 저장됨: {filename_wav}')
        # 녹음 직후 STT 변환
        self.audio_to_csv(filename_wav)

    def audio_to_csv(self, filepath):
        """음성 파일을 STT로 변환 후 CSV 저장"""
        recognizer = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language='ko-KR')
            except sr.UnknownValueError:
                text = '[인식 실패]'
            except sr.RequestError:
                text = '[STT 서버 오류]'

        csv_path = filepath.replace('.wav', '.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['시간', '텍스트'])
            writer.writerow([str(datetime.datetime.now().time())[:8], text])
        messagebox.showinfo('STT 완료', f'CSV 저장됨: {csv_path}')

    def search_keyword(self):
        """입력한 키워드로 CSV 검색"""
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning('오류', '검색할 키워드를 입력하세요.')
            return
        self.result_box.delete('1.0', tk.END)
        found = False
        for file in os.listdir(self.records_dir):
            if file.endswith('.csv'):
                with open(os.path.join(self.records_dir, file), 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # 헤더 건너뛰기
                    for row in reader:
                        if keyword in row[1]:
                            self.result_box.insert(tk.END, f'{file} | {row[0]} | {row[1]}\n')
                            found = True
        if not found:
            self.result_box.insert(tk.END, '검색 결과가 없습니다.\n')

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = JavisApp()
    app.run()
