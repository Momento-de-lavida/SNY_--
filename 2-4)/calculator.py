# calculator.py
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import sys

# -------------------------------
# 계산하는 로직만 담당하는 부분
# -------------------------------
class Calculator:
    def __init__(self):
        # 현재 화면에 보여지는 숫자
        self.current_input = '0'
        # 첫 번째 숫자
        self.first_operand = None
        # 어떤 연산을 할지(+, -, ×, ÷)
        self.operator = None
        # 두 번째 숫자를 기다리고 있는 상태인지
        self.waiting_for_second_operand = False

    # 사칙연산 함수들: 더하기, 빼기, 곱하기, 나누기
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        # 0으로 나누면 안되니까 'Error' 표시
        if b == 0:
            return 'Error'
        return a / b

    # 초기화, 음수/양수 바꾸기, 퍼센트 계산
    def reset(self):
        # 모두 초기 상태로 되돌리기
        self.current_input = '0'
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False

    def negative_positive(self):
        # 숫자가 0이 아니면 부호 바꾸기
        if self.current_input != '0':
            if self.current_input.startswith('-'):
                # 음수라면 '-' 없애서 양수로
                self.current_input = self.current_input[1:]
            else:
                # 양수라면 '-' 붙여서 음수로
                self.current_input = '-' + self.current_input

    def percent(self):
        # 현재 숫자를 100으로 나누기
        try:
            value = float(self.current_input)
            self.current_input = str(value / 100)
        except ValueError:
            self.current_input = 'Error'

    # 숫자를 입력할 때 화면에 숫자 추가
    def input_digit(self, digit):
        if self.waiting_for_second_operand:
            # 두 번째 숫자 입력이면 화면 새로 시작
            self.current_input = digit
            self.waiting_for_second_operand = False
        else:
            # 숫자가 15자리보다 길지 않으면 뒤에 붙이기
            if len(self.current_input) < 15:
                self.current_input = self.current_input + digit if self.current_input != '0' else digit

    # 소수점 입력
    def input_dot(self):
        # 이미 소수점이 없으면 붙이기
        if '.' not in self.current_input:
            self.current_input += '.'

    # 연산자 입력
    def set_operator(self, operator):
        if self.operator and not self.waiting_for_second_operand:
            # 이미 연산자가 있으면 먼저 계산
            self.equal()
        try:
            # 첫 번째 숫자 저장
            self.first_operand = float(self.current_input)
        except ValueError:
            self.first_operand = 0
        self.operator = operator
        self.waiting_for_second_operand = True

    # = 버튼 눌렀을 때 계산
    def equal(self):
        if self.operator and self.first_operand is not None:
            try:
                second_operand = float(self.current_input)
                if self.operator == '+':
                    result = self.add(self.first_operand, second_operand)
                elif self.operator == '−':
                    result = self.subtract(self.first_operand, second_operand)
                elif self.operator == '×':
                    result = self.multiply(self.first_operand, second_operand)
                elif self.operator == '÷':
                    result = self.divide(self.first_operand, second_operand)
                else:
                    result = second_operand
            except Exception:
                result = 'Error'

            # 소수점 6자리 이하로 반올림
            if isinstance(result, float) and result != 'Error':
                result = round(result, 6)
            self.current_input = str(result) if result != 'Error' else 'Error'

            # 계산 끝나면 초기화
            self.first_operand = None
            self.operator = None
            self.waiting_for_second_operand = False

# -------------------------------
# 계산기 화면과 버튼 담당 부분
# -------------------------------
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()  # 계산기 로직 불러오기
        self.initUI()

    def initUI(self):
        # 창 제목과 배경색
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setStyleSheet('background-color: #000000;')

        # 버튼을 격자 모양으로 배치
        self.layout = QGridLayout()
        self.layout.setSpacing(12)  # 버튼 사이 간격
        self.layout.setContentsMargins(15, 15, 15, 15)  # 테두리 여백

        # 숫자나 결과를 보여주는 화면
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 직접 입력 금지
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setFixedHeight(280)  # 높이 설정
        self.update_display()
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 정의 (텍스트, 위치, 배경색, 글자색)
        buttons = [
            ('AC', 1, 0, '#A5A5A5', 'black'), ('+/-', 1, 1, '#A5A5A5', 'black'), ('%', 1, 2, '#A5A5A5', 'black'), ('÷', 1, 3, '#FF9500', 'white'),
            ('7', 2, 0, '#333333', 'white'), ('8', 2, 1, '#333333', 'white'), ('9', 2, 2, '#333333', 'white'), ('×', 2, 3, '#FF9500', 'white'),
            ('4', 3, 0, '#333333', 'white'), ('5', 3, 1, '#333333', 'white'), ('6', 3, 2, '#333333', 'white'), ('−', 3, 3, '#FF9500', 'white'),
            ('1', 4, 0, '#333333', 'white'), ('2', 4, 1, '#333333', 'white'), ('3', 4, 2, '#333333', 'white'), ('+', 4, 3, '#FF9500', 'white'),
            ('.', 5, 2, '#333333', 'white'), ('=', 5, 3, '#FF9500', 'white')
        ]

        # 버튼 생성 및 배치
        for btn_text, row, col, bg_color, text_color in buttons:
            button = self.create_button(btn_text, bg_color, text_color)
            self.layout.addWidget(button, row, col)

        # 0 버튼은 가로 두 칸 차지
        zero_btn = self.create_button('0', '#333333', 'white', is_zero=True)
        self.layout.addWidget(zero_btn, 5, 0, 1, 2)

        self.setLayout(self.layout)
        self.setFixedSize(370, 650)  # 창 크기 고정

    # 버튼 만드는 함수
    def create_button(self, text, bg_color, text_color, is_zero=False):
        button = QPushButton(text)
        button_size = 78
        radius = button_size / 2  # 둥근 모양
        if is_zero:
            button.setFixedSize(button_size * 2 + self.layout.spacing(), button_size)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color}; color: {text_color};
                    border: none; border-radius: {radius}px;
                    font: bold 35px; text-align: left; padding-left: 28px;
                }}
                QPushButton:pressed {{ background-color: #777777; }}
            """)
        else:
            button.setFixedSize(button_size, button_size)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color}; color: {text_color};
                    border: none; border-radius: {radius}px;
                    font: bold 35px;
                }}
                QPushButton:pressed {{ background-color: #777777; }}
            """)
        button.clicked.connect(self.button_clicked)  # 클릭하면 함수 호출
        return button

    # 버튼 클릭했을 때
    def button_clicked(self):
        button = self.sender()
        text = button.text()
        if text in '0123456789':
            self.calc.input_digit(text)
        elif text == '.':
            self.calc.input_dot()
        elif text == 'AC':
            self.calc.reset()
        elif text in ['+', '−', '×', '÷']:
            self.calc.set_operator(text)
        elif text == '=':
            self.calc.equal()
        elif text == '%':
            self.calc.percent()
        elif text == '+/-':
            self.calc.negative_positive()
        self.update_display()

    # 화면 숫자 업데이트
    def update_display(self):
        number_string = str(self.calc.current_input)
        try:
            if number_string == 'Error':
                formatted_text = 'Error'
            elif '.' in number_string:
                integer_part, decimal_part = number_string.split('.')
                formatted_integer = f'{int(integer_part):,}'
                formatted_text = f'{formatted_integer}.{decimal_part}'
            else:
                formatted_text = f'{int(number_string):,}'
        except (ValueError, TypeError):
            formatted_text = number_string

        # 숫자가 길면 글자 크기 줄이기
        text_length = len(formatted_text)
        font_size = 80
        if text_length > 11:
            font_size = 45
        elif text_length > 9:
            font_size = 55
        elif text_length > 7:
            font_size = 70

        self.display.setStyleSheet(f"""
            font-size: {font_size}px;
            color: white;
            background-color: black;
            border: none;
            padding: 0 10px;
        """)
        self.display.setText(formatted_text)

# -------------------------------
# 프로그램 실행
# -------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())
