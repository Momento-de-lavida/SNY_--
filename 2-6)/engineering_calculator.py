import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics

# 공학용 계산기 클래스 정의
class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        # 창 타이틀과 초기 위치 및 크기 설정
        self.setWindowTitle('iPhone Engineering Calculator')
        self.setGeometry(100, 100, 700, 350)
        # 현재 디스플레이에 표시될 값 버퍼 초기화
        self.buffer = '0'
        # 메모리 값 초기화
        self.memory = 0
        # UI 구성 초기화 호출
        self.init_ui()

    def init_ui(self):
        # 배경색 설정
        self.setStyleSheet('background-color: black;')
        grid = QGridLayout()  # 버튼 및 디스플레이를 위한 그리드 레이아웃 생성
        grid.setSpacing(5)  # 버튼 간 간격 설정
        grid.setRowStretch(0, 1)  # 상단 디스플레이 영역 가중치
        grid.setRowStretch(1, 10) # 버튼 영역 가중치

        # 상단 표시줄(HBoxLayout) 생성
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(0)

        # 각도 단위 라벨(Rad) 설정
        self.rad_label = QLabel('Rad')
        self.rad_label.setFont(QFont('Segoe UI', 8))
        self.rad_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.rad_label.setStyleSheet('color: white; padding-left: 8px;')

        # 계산기 디스플레이 라벨 설정
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setStyleSheet('font-size: 60px; color: white; background-color: black; border: none;')
        self.display.setFont(QFont('Segoe UI', 60))
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.update_display()  # 초기 디스플레이 값 표시

        # 상단바 레이아웃에 라벨과 디스플레이 추가
        top_bar.addWidget(self.rad_label)
        top_bar.addStretch(1)
        top_bar.addWidget(self.display, 1)

        # 그리드에 상단바 배치
        grid.addLayout(top_bar, 0, 0, 1, 10)
        self._align_baselines()  # 라벨과 디스플레이 수평 정렬 맞춤

        # 버튼 정보 (라벨, 행, 열, (선택적) rowspan, colspan)
        buttons = [
            ('(', 1, 0), (')', 1, 1), ('mc', 1, 2), ('m+', 1, 3), ('m-', 1, 4), ('mr', 1, 5),
            ('AC', 1, 6), ('+/-', 1, 7), ('%', 1, 8), ('÷', 1, 9),
            ('2ⁿᵈ', 2, 0), ('x²', 2, 1), ('x³', 2, 2), ('xʸ', 2, 3), ('eˣ', 2, 4), ('10ˣ', 2, 5),
            ('7', 2, 6), ('8', 2, 7), ('9', 2, 8), ('×', 2, 9),
            ('1/x', 3, 0), ('√x', 3, 1), ('³√x', 3, 2), ('ʸ√x', 3, 3), ('ln', 3, 4), ('log₁₀', 3, 5),
            ('4', 3, 6), ('5', 3, 7), ('6', 3, 8), ('-', 3, 9),
            ('x!', 4, 0), ('sin', 4, 1), ('cos', 4, 2), ('tan', 4, 3), ('e', 4, 4), ('EE', 4, 5),
            ('1', 4, 6), ('2', 4, 7), ('3', 4, 8), ('+', 4, 9),
            ('Deg', 5, 0), ('sinh', 5, 1), ('cosh', 5, 2), ('tanh', 5, 3), ('π', 5, 4), ('Rand', 5, 5),
            ('0', 5, 6, 1, 2), ('.', 5, 8), ('=', 5, 9)
        ]

        # 폰트 정의
        font_main = QFont('Segoe UI', 15)
        font_small = QFont('Segoe UI', 8)
        font_gray = QFont('Segoe UI', 11, QFont.Bold)
        zero_btn = None  # 0 버튼 참조 저장

        # 버튼 생성 및 그리드 배치
        for label, row, col, *span in buttons:
            btn = QPushButton(label)
            # 폰트 설정
            if label == 'log₁₀':
                btn.setFont(QFont('Segoe UI Symbol', 8))
            elif label in ('0','1','2','3','4','5','6','7','8','9','.','÷','×','-','+','='):
                btn.setFont(font_main)
            elif label in ('AC', '+/-', '%'):
                btn.setFont(font_gray)
            else:
                btn.setFont(font_small)

            btn.setFixedSize(65, 50)  # 기본 버튼 크기 설정

            # rowspan, colspan 적용
            if span:
                grid.addWidget(btn, row, col, span[0], span[1])
                if label == '0':
                    btn.setFixedSize(135, 50)  # 0 버튼 넓게 표시
                    zero_btn = btn
            else:
                grid.addWidget(btn, row, col)

            # 버튼 색상 스타일 지정
            if label in ('AC', '+/-', '%'):
                btn.setStyleSheet('background-color: rgb(165,165,165); color: black; border-radius: 25px;')
            elif label in ('÷','×','-','+','='):
                btn.setStyleSheet('background-color: rgb(255,159,10); color: white; border-radius: 25px;')
            else:
                btn.setStyleSheet('background-color: rgb(50,50,50); color: white; border-radius: 25px;')

            # 버튼 클릭 이벤트 연결
            if label == 'log₁₀':
                btn.clicked.connect(self.on_log10_clicked)
            elif label == 'mc':
                btn.clicked.connect(self.on_mc_clicked)
            elif label == 'm+':
                btn.clicked.connect(self.on_mplus_clicked)
            elif label == 'm-':
                btn.clicked.connect(self.on_mminus_clicked)
            elif label == 'mr':
                btn.clicked.connect(self.on_mr_clicked)
            else:
                btn.clicked.connect(lambda checked, b=label: self.on_button_clicked(b))

        # 0 버튼에 특별 레이블 처리
        if zero_btn is not None:
            zero_btn.setText('')  # 기본 텍스트 제거
            zlbl = QLabel('0', parent=zero_btn)
            zlbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            zlbl.setStyleSheet('color: white; padding-left: 24px;')
            zlbl.setFont(font_main)
            zlbl.setGeometry(0, 0, zero_btn.width(), zero_btn.height())
            zlbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 클릭 이벤트 투과

        # 전체 레이아웃 설정
        self.setLayout(grid)

    # 라벨과 디스플레이의 기준선 정렬
    def _align_baselines(self):
        fm_rad = QFontMetrics(self.rad_label.font())
        fm_disp = QFontMetrics(self.display.font())
        target = max(fm_rad.descent(), fm_disp.descent())
        rad_pad = max(0, target - fm_rad.descent())
        disp_pad = max(0, target - fm_disp.descent())
        self.rad_label.setStyleSheet(f"color: white; padding-left: 8px; padding-bottom: {rad_pad}px;")
        self.display.setStyleSheet(f"font-size: 60px; color: white; background-color: black; border: none; padding-bottom: {disp_pad}px;")

    # 디스플레이 문자열을 HTML로 변환하여 위첨자/아래첨자 처리
    def render_html(self, text: str) -> str:
        html = (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        html = html.replace('x²', 'x<span style="vertical-align:super; font-size:0.6em">2</span>')
        html = html.replace('x³', 'x<span style="vertical-align:super; font-size:0.6em">3</span>')
        html = html.replace('log10(', 'log<span style="vertical-align:sub; font-size:0.5em">10</span>(')
        return html

    # 디스플레이 갱신
    def update_display(self):
        self.display.setTextFormat(Qt.RichText)
        self.display.setText(self.render_html(self.buffer if self.buffer else '0'))

    # ---------- 계산 기능 정의 ----------
    def sin_func(self, x): return math.sin(x)
    def cos_func(self, x): return math.cos(x)
    def tan_func(self, x): return math.tan(x)
    def sinh_func(self, x): return math.sinh(x)
    def cosh_func(self, x): return math.cosh(x)
    def tanh_func(self, x): return math.tanh(x)
    def square_func(self, x): return x**2
    def cube_func(self, x): return x**3
    def pi_func(self): return math.pi

    # ---------- 버튼 클릭 이벤트 핸들러 ----------
    def on_button_clicked(self, label):
        # 초기 버퍼 0 처리
        if self.buffer == '0' and label not in {'0', '.'}:
            self.buffer = ''

        # AC 버튼 초기화
        if label == 'AC':
            self.buffer = '0'
        # = 버튼 계산 처리
        elif label == '=':
            try:
                # 안전한 eval 환경 설정
                safe_dict = {
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                    'pi': math.pi, 'sqrt': math.sqrt, 'log10': math.log10,
                    'pow': pow, 'e': math.e
                }
                expr = self.buffer.replace('×','*').replace('÷','/').replace('^','**')
                self.buffer = str(eval(expr, {'__builtins__': None}, safe_dict))
            except:
                self.buffer = 'Error'
        # 삼각함수 및 하이퍼볼릭 함수 처리
        elif label in {'sin','cos','tan','sinh','cosh','tanh'}:
            self.buffer += label + '('
        # 원주율 처리
        elif label == 'π':
            self.buffer += str(math.pi)
        else:
            self.buffer += label

        self.update_display()

    # log10 버튼 처리
    def on_log10_clicked(self):
        if self.buffer == '0':
            self.buffer = ''
        self.buffer += 'log10('
        self.update_display()

    # 메모리 초기화
    def on_mc_clicked(self):
        self.memory = 0

    # 메모리 더하기
    def on_mplus_clicked(self):
        try:
            self.memory += float(eval(self.buffer))
        except:
            pass

    # 메모리 빼기
    def on_mminus_clicked(self):
        try:
            self.memory -= float(eval(self.buffer))
        except:
            pass

    # 메모리 호출
    def on_mr_clicked(self):
        self.buffer = str(self.memory)
        self.update_display()

# 프로그램 실행부
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    calc.show()
    sys.exit(app.exec_())
