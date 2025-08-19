import os  # 파일 및 디렉토리 경로를 다루기 위한 모듈
import zipfile  # zip 파일 압축 해제를 위한 모듈
import cv2  # OpenCV: 이미지 처리 및 사람 탐지에 사용
from tkinter import Tk, Label  # GUI 창과 이미지 표시를 위한 tkinter 모듈
from PIL import Image, ImageTk  # OpenCV 이미지를 tkinter에서 보여주기 위한 변환 도구

class MasImageHelper:
    def __init__(self, zip_path, folder_name='CCTV'):
        # 초기 설정: zip 파일 경로와 압축 해제할 폴더 이름 지정
        self.zip_path = zip_path
        self.folder_name = folder_name
        self.images = []  # 이미지 파일 경로들을 저장할 리스트
        self.index = 0  # 현재 검사 중인 이미지 인덱스
        self.window = None  # tkinter 창 객체
        self.label = None  # 이미지 표시용 라벨
        self.hog = cv2.HOGDescriptor()  # HOG 기반 사람 탐지기 생성
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  # 기본 사람 탐지 모델 설정

    def extract_zip(self):
        # zip 파일을 지정된 폴더에 압축 해제
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.folder_name)

    def load_images(self):
        # 지정된 폴더에서 이미지 파일(.png, .jpg, .jpeg)만 골라 리스트에 저장
        self.images = [
            os.path.join(self.folder_name, file)
            for file in os.listdir(self.folder_name)
            if file.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

    def detect_people(self, image_path):
        # 이미지 파일을 불러와서 사람을 탐지
        image = cv2.imread(image_path)  # 이미지 읽기
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 흑백으로 변환 (탐지 성능 향상)

        # 사람 탐지: 여러 크기의 윈도우로 스캔하여 사람 위치(boxes) 반환
        boxes, _ = self.hog.detectMultiScale(gray)

        # 탐지된 사람 위치에 빨간 사각형 그리기
        for (x, y, w, h) in boxes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # 사람이 탐지된 경우 이미지 반환, 없으면 None 반환
        return image if len(boxes) > 0 else None

    def show_image(self, image_cv):
        # OpenCV 이미지(BGR)를 tkinter에서 보여줄 수 있도록 변환
        image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)  # RGB로 변환
        image_pil = Image.fromarray(image_rgb)  # PIL 이미지로 변환
        image_pil = image_pil.resize((800, 600))  # 보기 좋게 크기 조절
        photo = ImageTk.PhotoImage(image_pil)  # tkinter용 이미지 객체 생성

        # 라벨에 이미지 표시
        self.label.config(image=photo)
        self.label.image = photo  # 이미지가 사라지지 않도록 참조 유지

    def search_next(self, event=None):
        # 이미지 리스트를 순차적으로 탐색하며 사람을 찾음
        while self.index < len(self.images):
            image_path = self.images[self.index]
            print('검사 중:', image_path)  # 현재 검사 중인 이미지 경로 출력
            result = self.detect_people(image_path)  # 사람 탐지 시도
            self.index += 1  # 다음 이미지로 이동

            if result is not None:
                self.show_image(result)  # 사람이 있으면 이미지 표시
                return  # 탐지 성공 시 루프 종료

        # 모든 이미지 검사 완료 후 메시지 출력
        print('검색 완료')
        self.label.config(text='검색 완료')

    def run_viewer(self):
        # 전체 프로그램 실행 흐름
        self.extract_zip()  # zip 파일 압축 해제
        self.load_images()  # 이미지 파일 로딩

        # tkinter GUI 창 생성 및 설정
        self.window = Tk()
        self.window.title('사람을 찾아라 - CCTV 분석기')

        # 이미지 표시용 라벨 생성 및 배치
        self.label = Label(self.window)
        self.label.pack()

        # 엔터 키를 누르면 다음 이미지 탐색
        self.window.bind('<Return>', self.search_next)

        self.search_next()  # 첫 번째 이미지부터 탐색 시작

        self.window.mainloop()  # GUI 이벤트 루프 시작

# 프로그램 실행: CCTV.zip 파일을 분석
helper = MasImageHelper('CCTV.zip')
helper.run_viewer()