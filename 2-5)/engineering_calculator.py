# engineering_calculator.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Engineering Calculator')
        self.setGeometry(100, 100, 700, 350)
        self.buffer = '0'  # 디스플레이 내부 평문 버퍼
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('background-color: black;')

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setRowStretch(0, 10)
        grid.setRowStretch(1, 1)

        # 상단 Rnd 라벨
        rad = QLabel('Rad')
        rad.setFont(QFont('Segoe UI', 10))
        rad.setStyleSheet('color: white; padding-left: 5px; padding-top: 15px;')
        rad.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        grid.addWidget(rad, 0, 0, 1, 1)

        # 디스플레이 (QLabel + RichText)
        self.display = QLabel()
        self.display.setFixedSize(620, 80)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setStyleSheet('font-size: 50px; color: white; background-color: black; border: none;')
        self.display.setFont(QFont('Segoe UI', 60))
        self.update_display()
        grid.addWidget(self.display, 0, 1, 1, 9)

        buttons = [
            # 1행
            ('(', 1, 0), (')', 1, 1), ('mc', 1, 2), ('m+', 1, 3), ('m-', 1, 4), ('mr', 1, 5),
            ('AC', 1, 6), ('+/-', 1, 7), ('%', 1, 8), ('÷', 1, 9),
            # 2행
            ('2ⁿᵈ', 2, 0), ('x²', 2, 1), ('x³', 2, 2), ('xʸ', 2, 3), ('eˣ', 2, 4), ('10ˣ', 2, 5),
            ('7', 2, 6), ('8', 2, 7), ('9', 2, 8), ('×', 2, 9),
            # 3행
            ('1/x', 3, 0), ('√x', 3, 1), ('³√x', 3, 2), ('ʸ√x', 3, 3), ('ln', 3, 4), ('log₁₀', 3, 5),
            ('4', 3, 6), ('5', 3, 7), ('6', 3, 8), ('-', 3, 9),
            # 4행
            ('x!', 4, 0), ('sin', 4, 1), ('cos', 4, 2), ('tan', 4, 3), ('e', 4, 4), ('EE', 4, 5),
            ('1', 4, 6), ('2', 4, 7), ('3', 4, 8), ('+', 4, 9),
            # 5행
            ('Deg', 5, 0), ('sinh', 5, 1), ('cosh', 5, 2), ('tanh', 5, 3), ('π', 5, 4), ('Rand', 5, 5),
            ('0', 5, 6, 1, 2), ('.', 5, 8), ('=', 5, 9)
        ]

        font_main = QFont('Segoe UI', 15)
        font_small = QFont('Segoe UI', 8)
        font_gray  = QFont('Segoe UI', 11, QFont.Bold)

        # 0 버튼을 나중에 커스텀하기 위해 참조 저장
        zero_btn = None

        for label, row, col, *span in buttons:
            btn = QPushButton(label)

            # log₁₀: 유니코드 아래첨자 + 폰트 고정(벌어짐 방지)
            if label == 'log₁₀':
                btn.setFont(QFont('Segoe UI Symbol', 8))
            elif label in ('0','1','2','3','4','5','6','7','8','9','.','÷','×','-','+','='):
                btn.setFont(font_main)
            elif label in ('AC', '+/-', '%'):
                btn.setFont(font_gray)
            else:
                btn.setFont(font_small)

            btn.setFixedSize(65, 50)
            if span:
                grid.addWidget(btn, row, col, span[0], span[1])
                if label == '0':
                    # 두 칸 폭
                    btn.setFixedSize(135, 50)
                    zero_btn = btn  # 나중에 라벨 덧씌움
            else:
                grid.addWidget(btn, row, col)

            # 색상
            if label in ('AC', '+/-', '%'):
                btn.setStyleSheet('background-color: rgb(165,165,165); color: black; border-radius: 25px;')
            elif label in ('÷','×','-','+','='):
                btn.setStyleSheet('background-color: rgb(255,159,10); color: white; border-radius: 25px;')
            else:
                btn.setStyleSheet('background-color: rgb(50,50,50); color: white; border-radius: 25px;')

            # 클릭 연결
            if label == 'log₁₀':
                btn.clicked.connect(self.on_log10_clicked)
            else:
                btn.clicked.connect(self.on_button_clicked)

        # --- 0 버튼 텍스트 왼쪽 정렬: 자식 QLabel로 표시(마우스 투명) ---
        if zero_btn is not None:
            zero_btn.setText('')  # 버튼 자체 텍스트 제거(가운데 정렬 방지)
            zlbl = QLabel('0', parent=zero_btn)
            zlbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            zlbl.setStyleSheet('color: white; padding-left: 24px;')  # 원하는 x 위치로
            zlbl.setFont(font_main)
            zlbl.setGeometry(0, 0, zero_btn.width(), zero_btn.height())
            zlbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.setLayout(grid)

    # ---------- 디스플레이 렌더 ----------
    def render_html(self, text: str) -> str:
        html = (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

    # log10( 전체를 축소 + 아래첨자 10은 더 작게
        html = html.replace(
            'log10(',
            '<span style="font-size:0.2em;">'
            'log<span style="vertical-align:sub; font-size:0.15em;">10</span>('
            '</span>'
        )

    # 나머지 지수 표현
        html = html.replace(
            'x²', 'x<span style="vertical-align:super; font-size:0.60em">2</span>'
        )
        html = html.replace(
            'x³', 'x<span style="vertical-align:super; font-size:0.60em">3</span>'
        )
        return html

    def update_display(self):
        self.display.setTextFormat(Qt.RichText)
        self.display.setText(self.render_html(self.buffer if self.buffer else '0'))

    # ---------- 핸들러 ----------
    def on_log10_clicked(self):
        cur = self.buffer
        if cur == '0':
            cur = ''
        self.buffer = cur + 'log10('   # 내부는 평문
        self.update_display()

    def on_button_clicked(self):
        sender = self.sender()
        btn = sender.text()
        cur = self.buffer

        if cur == '0' and btn not in {'0', '.'}:
            cur = ''

        if btn == 'AC':
            self.buffer = '0'
            self.update_display()
            return

        if btn == '=':
            return  # 계산 미구현

        binary_ops = {'÷', '×', '-', '+', '%'}
        unary_funcs = {'sin', 'cos', 'tan', 'ln'}

        if btn in unary_funcs:
            self.buffer = cur + f'{btn}('
            self.update_display()
            return

        if btn in binary_ops:
            self.buffer = (cur + ' ' + btn).strip()
            self.update_display()
            return

        if cur == '0' and btn.isdigit():
            self.buffer = btn
        else:
            self.buffer = cur + btn

        self.update_display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    calc.show()
    sys.exit(app.exec_())
