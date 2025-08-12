import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    # Calculator 클래스: PyQt5의 QWidget을 상속받아 계산기 UI와 로직을 구현합니다.
    def __init__(self):
        super().__init__()
        # 인스턴스 변수 초기화
        # 현재 화면에 표시되는 숫자를 저장합니다. 초기값은 '0'입니다.
        self.current_input = '0'
        # 첫 번째 피연산자(계산에 사용되는 첫 번째 숫자)를 저장합니다.
        self.first_operand = None
        # 현재 선택된 연산자(+, -, *, /)를 저장합니다.
        self.operator = None
        # 두 번째 피연산자를 입력받을 준비가 되었는지 여부를 나타냅니다.
        self.waiting_for_second_operand = False
        # UI를 초기화하는 메서드를 호출합니다.
        self.initUI()

    def initUI(self):
        """UI 초기 설정"""
        # 창의 제목을 'iPhone 스타일 계산기'로 설정합니다.
        self.setWindowTitle('iPhone 스타일 계산기')
        # 위젯의 배경색을 검은색으로 설정합니다.
        self.setStyleSheet('background-color: #000000;')
        
        # 메인 레이아웃 설정: QGridLayout을 사용하여 버튼을 격자 형태로 배치합니다.
        self.layout = QGridLayout()
        # 위젯 간의 간격을 12픽셀로 설정합니다.
        self.layout.setSpacing(12)
        # 레이아웃의 외부 여백을 상, 하, 좌, 우 15픽셀로 설정합니다.
        self.layout.setContentsMargins(15, 15, 15, 15)

        # --- 출력창 ---
        # 숫자를 표시할 QLineEdit 위젯을 생성합니다.
        self.display = QLineEdit()
        # 사용자가 직접 입력할 수 없도록 읽기 전용으로 설정합니다.
        self.display.setReadOnly(True)
        # 텍스트를 오른쪽 정렬로 설정합니다.
        self.display.setAlignment(Qt.AlignRight)
        
        # 숫자 출력 공간의 높이를 280픽셀로 설정하여 더 넓게 만듭니다. (사용자 요청 반영)
        self.display.setFixedHeight(280)
        
        # update_display를 호출하여 초기 텍스트와 폰트 크기를 설정합니다.
        self.update_display()
        
        # 출력창을 0행 0열에 배치하고, 1행 4열을 차지하도록 설정합니다.
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        # --- 버튼 생성 및 배치 ---
        # 버튼의 텍스트, 위치(행, 열), 배경색, 텍스트 색상을 리스트에 정의합니다.
        buttons = [
            ('AC', 1, 0, '#A5A5A5', 'black'), ('+/-', 1, 1, '#A5A5A5', 'black'), ('%', 1, 2, '#A5A5A5', 'black'), ('÷', 1, 3, '#FF9500', 'white'),
            ('7', 2, 0, '#333333', 'white'), ('8', 2, 1, '#333333', 'white'), ('9', 2, 2, '#333333', 'white'), ('×', 2, 3, '#FF9500', 'white'),
            ('4', 3, 0, '#333333', 'white'), ('5', 3, 1, '#333333', 'white'), ('6', 3, 2, '#333333', 'white'), ('−', 3, 3, '#FF9500', 'white'),
            ('1', 4, 0, '#333333', 'white'), ('2', 4, 1, '#333333', 'white'), ('3', 4, 2, '#333333', 'white'), ('+', 4, 3, '#FF9500', 'white'),
            ('.', 5, 2, '#333333', 'white'), ('=', 5, 3, '#FF9500', 'white')
        ]

        # 리스트에 정의된 정보를 기반으로 버튼을 생성하고 레이아웃에 추가합니다.
        for btn_text, row, col, bg_color, text_color in buttons:
            button = self.create_button(btn_text, bg_color, text_color)
            self.layout.addWidget(button, row, col)

        # --- '0' 버튼 특별 처리 ---
        # '0' 버튼은 너비가 두 배이므로 특별히 처리합니다.
        zero_btn = self.create_button('0', '#333333', 'white', is_zero=True)
        # '0' 버튼을 5행 0열에 배치하고, 1행 2열을 차지하도록 설정합니다.
        self.layout.addWidget(zero_btn, 5, 0, 1, 2)

        # 위젯의 레이아웃을 설정합니다.
        self.setLayout(self.layout)
        # 창의 크기를 고정합니다.
        self.setFixedSize(370, 650)

    def create_button(self, text, bg_color, text_color, is_zero=False):
        """버튼을 생성하고 스타일을 적용하는 헬퍼 함수"""
        button = QPushButton(text)
        button_size = 78
        
        if is_zero:
            # '0' 버튼은 너비를 두 배로 설정합니다.
            button.setFixedSize(button_size * 2 + self.layout.spacing(), button_size)
            # '0' 버튼에 맞는 스타일을 적용합니다.
            radius = button_size / 2
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg_color}; color: {text_color};
                    border: none; border-radius: {radius}px;
                    font: bold 35px; text-align: left; padding-left: 28px;
                }}
                QPushButton:pressed {{ background-color: #777777; }}
                """
            )
        else:
            # 나머지 버튼들은 정사각형으로 설정합니다.
            button.setFixedSize(button_size, button_size)
            # 원형 버튼 스타일을 적용합니다.
            radius = button_size / 2
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg_color}; color: {text_color};
                    border: none; border-radius: {radius}px;
                    font: bold 35px;
                }}
                QPushButton:pressed {{ background-color: #777777; }}
                """
            )
        
        # 버튼 클릭 시 button_clicked 메서드를 호출하도록 연결합니다.
        button.clicked.connect(self.button_clicked)
        return button

    def button_clicked(self):
        """버튼 클릭 시 호출되는 슬롯 함수"""
        # 클릭된 버튼 객체를 가져옵니다.
        button = self.sender()
        # 버튼의 텍스트를 가져옵니다.
        text = button.text()

        # 클릭된 버튼의 텍스트에 따라 적절한 메서드를 호출합니다.
        if text in '0123456789':
            self.input_digit(text)
        elif text == '.':
            self.input_dot()
        elif text == 'AC':
            self.reset_calculator()
        elif text in ['+', '−', '×', '÷']:
            self.perform_operation(text)
        elif text == '=':
            self.calculate_result()
        elif text == '%':
            self.calculate_percentage()
        elif text == '+/-':
            self.toggle_sign()
        
        # 변경된 내용을 디스플레이에 업데이트합니다.
        self.update_display()

    def input_digit(self, digit):
        # 두 번째 피연산자를 기다리는 중이면 현재 입력값을 새 숫자로 바꿉니다.
        if self.waiting_for_second_operand:
            self.current_input = digit
            self.waiting_for_second_operand = False
        else:
            # 현재 입력값의 길이가 15자 미만일 때만 숫자를 추가합니다.
            if len(self.current_input) < 15:
                # 현재 입력값이 '0'이면 새 숫자로 바꾸고, 아니면 뒤에 숫자를 추가합니다.
                self.current_input = self.current_input + digit if self.current_input != '0' else digit

    def input_dot(self):
        # 현재 입력값에 소수점(.)이 없으면 추가합니다.
        if '.' not in self.current_input:
            self.current_input += '.'

    def reset_calculator(self):
        # 모든 인스턴스 변수를 초기 상태로 되돌립니다.
        self.current_input = '0'
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False

    def perform_operation(self, next_operator):
        # 이전에 연산자가 있고, 두 번째 피연산자를 기다리지 않는 상태라면 계산을 먼저 수행합니다.
        if self.operator and not self.waiting_for_second_operand:
            self.calculate_result()
            self.update_display()

        # 현재 입력값을 첫 번째 피연산자로 저장합니다. (콤마 제거 후 float로 변환)
        self.first_operand = float(self.current_input.replace(',', ''))
        # 새로운 연산자를 저장합니다.
        self.operator = next_operator
        # 다음 입력은 두 번째 피연산자이므로 상태를 변경합니다.
        self.waiting_for_second_operand = True

    def calculate_result(self):
        # 연산자와 첫 번째 피연산자가 모두 존재할 때만 계산을 수행합니다.
        if self.operator and self.first_operand is not None:
            # calculate 메서드를 호출하여 결과를 얻습니다.
            result = self.calculate()
            # 결과값을 포맷팅하여 현재 입력값에 저장합니다.
            self.current_input = self.format_result(result)
            # 계산 완료 후 상태를 초기화합니다.
            self.first_operand = None
            self.operator = None
            self.waiting_for_second_operand = False

    def calculate(self):
        # 현재 입력값을 두 번째 피연산자로 가져옵니다. (콤마 제거 후 float로 변환)
        second_operand = float(self.current_input.replace(',', ''))
        # 저장된 연산자에 따라 계산을 수행하고 결과를 반환합니다.
        if self.operator == '+':
            return self.first_operand + second_operand
        if self.operator == '−':
            return self.first_operand - second_operand
        if self.operator == '×':
            return self.first_operand * second_operand
        if self.operator == '÷':
            # 0으로 나누는 경우 'Error'를 반환합니다.
            if second_operand == 0: return 'Error'
            return self.first_operand / second_operand
        return second_operand

    def calculate_percentage(self):
        # 현재 입력값을 100으로 나눈 후 포맷팅하여 저장합니다.
        value = float(self.current_input.replace(',', ''))
        self.current_input = self.format_result(value / 100)

    def toggle_sign(self):
        # 현재 입력값이 '0'이 아닐 때만 부호를 변경합니다.
        if self.current_input != '0':
            # 음수면 마이너스 부호를 제거합니다.
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            # 양수면 마이너스 부호를 추가합니다.
            else:
                self.current_input = '-' + self.current_input

    def update_display(self):
        """디스플레이의 폰트 크기를 조절하고 텍스트에 1,000단위 콤마를 추가하여 업데이트합니다."""
        number_string = str(self.current_input)
        
        # 1,000 단위 콤마 포맷팅
        try:
            if number_string == 'Error':
                formatted_text = 'Error'
            elif '.' in number_string:
                # 소수점이 포함된 경우, 정수 부분에만 콤마를 적용합니다.
                integer_part, decimal_part = number_string.split('.')
                formatted_integer = f'{int(integer_part):,}'
                formatted_text = f'{formatted_integer}.{decimal_part}'
            else:
                # 정수인 경우 콤마를 적용합니다.
                formatted_text = f'{int(number_string):,}'
        except (ValueError, TypeError):
            # 숫자로 변환할 수 없는 경우, 원본 텍스트를 그대로 사용합니다.
            formatted_text = number_string

        # 폰트 크기 동적 조절
        text_length = len(formatted_text)
        font_size = 80
        # 텍스트 길이에 따라 폰트 크기를 조절하여 출력창을 벗어나지 않게 합니다.
        if text_length > 11:
            font_size = 45
        elif text_length > 9:
            font_size = 55
        elif text_length > 7:
            font_size = 70
            
        # 스타일시트를 적용하여 폰트 크기, 색상, 배경색, 여백 등을 설정합니다.
        self.display.setStyleSheet(
            f"""
            font-size: {font_size}px;
            color: white;
            background-color: black;
            border: none;
            padding: 0 10px;
            """
        )
        # 최종 포맷팅된 텍스트를 디스플레이에 설정합니다.
        self.display.setText(formatted_text)
        
    def format_result(self, result):
        if result == 'Error':
            return 'Error'
        # 결과가 소수점 이하가 있는 부동소수점일 경우
        if isinstance(result, float) and not result.is_integer():
             # 소수점 8자리까지 표시하고, 뒤에 따라오는 0은 제거합니다.
             return f"{result:.8f}".rstrip('0').rstrip('.')

        # 결과가 정수이거나 다른 타입일 경우
        return str(int(result)) if isinstance(result, float) else str(result)

if __name__ == '__main__':
    # 애플리케이션 객체를 생성합니다.
    app = QApplication(sys.argv)
    # Calculator 클래스의 인스턴스를 생성합니다.
    calc = Calculator()
    # 계산기 창을 화면에 표시합니다.
    calc.show()
    # 애플리케이션의 이벤트 루프를 시작합니다.
    sys.exit(app.exec_())
