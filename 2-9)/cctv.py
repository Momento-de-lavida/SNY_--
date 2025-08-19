import os  # 폴더와 파일을 다루는 기본 도구
import zipfile  # zip 파일을 풀기 위한 도구
from tkinter import Tk, Label  # 화면을 만들기 위한 도구
from PIL import Image, ImageTk  # 이미지를 읽고 보여주는 도구 (설치 필요: Pillow)

# 이미지를 처리하는 기능을 담은 클래스예요
class MasImageHelper:
    def __init__(self, zip_path, folder_name='CCTV'):
        self.zip_path = zip_path  # zip 파일 경로
        self.folder_name = folder_name  # 압축을 풀 폴더 이름
        self.images = []  # 이미지 파일 경로들을 저장할 리스트
        self.index = 0  # 현재 보여줄 이미지의 번호
        self.window = None  # tkinter 창
        self.label = None  # 이미지를 보여줄 라벨

    def extract_zip(self):
        # zip 파일을 지정된 폴더에 풀어요
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.folder_name)

    def load_images(self):
        # 폴더 안의 이미지 파일들을 리스트에 저장해요
        self.images = [
            os.path.join(self.folder_name, file)
            for file in os.listdir(self.folder_name)
            if file.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        print('불러온 이미지 수:', len(self.images))  # 디버깅용 출력

    def show_image(self):
        # 현재 인덱스의 이미지를 화면에 보여줘요
        if not self.images:
            print('이미지가 없어요.')
            return

        image_path = self.images[self.index]
        print('보여줄 이미지:', image_path)  # 디버깅용 출력

        image = Image.open(image_path)

        # 이미지 크기를 조절해서 화면에 잘 보이게 해요
        image = image.resize((800, 600))  # 필요에 따라 크기 조절 가능

        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # 이미지가 사라지지 않도록 유지해요

    def next_image(self, event=None):
        # 오른쪽 키를 누르면 다음 이미지를 보여줘요
        if self.index < len(self.images) - 1:
            self.index += 1
            self.show_image()

    def prev_image(self, event=None):
        # 왼쪽 키를 누르면 이전 이미지를 보여줘요
        if self.index > 0:
            self.index -= 1
            self.show_image()

    def run_viewer(self):
        # 이미지 뷰어를 실행하는 함수예요
        self.extract_zip()  # zip 파일을 풀어요
        self.load_images()  # 이미지들을 불러와요

        self.window = Tk()  # tkinter 화면을 만들어요
        self.window.title('MasImageHelper 이미지 뷰어')  # 창 제목을 정해요

        self.label = Label(self.window)  # 이미지를 보여줄 라벨을 만들어요
        self.label.pack()  # 화면에 라벨을 배치해요

        self.show_image()  # 첫 번째 이미지를 보여줘요

        # 방향키를 눌렀을 때 어떤 동작을 할지 정해요
        self.window.bind('<Right>', self.next_image)
        self.window.bind('<Left>', self.prev_image)

        self.window.mainloop()  # 화면을 계속 보여줘요

# 프로그램을 실행해요
helper = MasImageHelper('CCTV.zip')  # CCTV.zip 파일을 사용해요
helper.run_viewer()  # 이미지 뷰어를 실행해요
