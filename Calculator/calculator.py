import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('./calculator.ui')[0]  # UI 파일(XML)을 파이썬 코드로 불러오기


class Exam(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.first_input_flag = False  # 첫 번째 입력 flag
        self.btn_all_clear_clicked_slot()
        self.opcode = ''
        self.buffer = self.lbl_buffer.text()
        self.math_exp = list()   # 계산 수식을 담을 리스트

    def initUI(self):
        for n in range(0, 10):
            getattr(self, "btn_%s" % n).clicked.connect(self.btn_number_process)

        self.btn_add.clicked.connect(self.btn_opcode_process)
        self.btn_sub.clicked.connect(self.btn_opcode_process)
        self.btn_mul.clicked.connect(self.btn_opcode_process)
        self.btn_div.clicked.connect(self.btn_opcode_process)

        self.btn_equal.clicked.connect(self.btn_opcode_process)

        self.btn_all_clear.clicked.connect(self.btn_all_clear_clicked_slot)
        self.btn_clear.clicked.connect(self.btn_clear_clicked_slot)
        self.btn_back.clicked.connect(self.btn_back_clicked_slot)
        self.btn_point.clicked.connect(self.btn_point_process)

    # 숫자 버튼을 눌렀을 때
    def btn_number_process(self):
        self.btn_disable_process(True)

        if self.lbl_result.text() == '0':
            self.first_input_flag = True

        if self.first_input_flag:
            self.first_input_flag = False
            self.lbl_result.setText('')

        if self.opcode == '=':
            self.lbl_buffer.clear()
            self.math_exp.clear()
            self.lbl_result.setText('')
            self.opcode = ''

        # 클릭한 버튼 값을 화면에 출력
        text = self.lbl_result.text()
        self.lbl_result.setText(text + self.sender().text())

    # . 을 입력했을 경우
    def btn_point_process(self):
        if self.opcode == '=':
            self.opcode = ''

        if self.first_input_flag:
            self.lbl_result.setText('0')

        self.first_input_flag = False
        str_lbl = self.lbl_result.text()

        if '.' not in self.lbl_result.text():
            self.lbl_result.setText(str_lbl + '.')

    # 계산 수식을 라벨에 출력
    def lbl_buffer_process(self, number, opcode):
        if number == float("inf"):
            self.number = 0.0
            return 0.0
        self.math_exp.append(str(number))
        self.math_exp.append(opcode)
        lbl_buffer = ''
        result = ''

        for item in self.math_exp:
            lbl_buffer += item + ' '
        self.lbl_buffer.setText(lbl_buffer)

        if self.math_exp[-1] == '=':
            self.math_exp.clear()
            result = self.lbl_result.text()
        return result

    # infinity 값일 때 버튼 비활성화
    def btn_disable_process(self, stat):
        buttons = ['add', 'sub', 'mul', 'div',
                   'point', 'back', 'clear']

        for item in buttons:
            getattr(self, 'btn_%s' % item).setEnabled(stat)

    # 연산자를 눌렀을 때
    def btn_opcode_process(self):
        # 연산자를 연속으로 눌렀을 때
        if self.first_input_flag:
            self.opcode = self.sender().text()
            self.math_exp = self.math_exp[:len(self.math_exp) - 2]

        else:
            self.first_input_flag = True  # 첫 번째 피연산자 입력이 끝나면 flag 값 변경
            self.number = float(self.lbl_result.text())
            self.lbl_result.setText(str(self.number))
            if self.opcode != '':
                self.calculate()
            self.result = float(self.lbl_result.text())

            # infinity 값일 경우, 더이상 진행할 수 없도록 버튼 비활성화
            if self.result == float('inf'):
                self.lbl_result.setText('inf')
                self.opcode = '='
                self.btn_disable_process(False)

            self.opcode = self.sender().text()  # 눌린 버튼 저장.

        if self.lbl_buffer_process(self.number, self.opcode):
            self.first_input_flag = False
            self.buffer = ''

    # 입력 값 계산
    def calculate(self):
        if self.opcode == '+':
            self.result = self.result + self.number
        elif self.opcode == '-':
            self.result = self.result - self.number
        elif self.opcode == '*':
            self.result = self.result * self.number
        elif self.opcode == '/':
            if self.lbl_result.text() == '0.0':
                self.result = float('inf')
            else:
                self.result = self.result / self.number
        elif self.opcode == '=':
            self.result = float(self.lbl_result.text())
            if self.result == float('inf'):
                self.btn_disable_process(True)
                self.result = 0

            self.math_exp.clear()
        self.lbl_result.setText(str(self.result))
        self.lbl_buffer.clear()

    # '=' 버튼을 눌렀을 때
    def btn_equal_clicked_process(self):
        self.first_input_flag = True
        self.calculate()
        self.opcode = '='  # '=' 를 눌렀을때 결과값이 출력 되도록 하기 위해선 op연산자를 초기화 해야 함.

    # AC 버튼을 눌렀을 때
    def btn_all_clear_clicked_slot(self):
        self.btn_disable_process(True)
        self.number = 0
        self.opcode = '='
        self.lbl_result.setText('0')
        self.lbl_buffer.setText('')
        self.first_input_flag = False

    # C 버튼을 눌렀을 때
    def btn_clear_clicked_slot(self):
        self.lbl_result.setText('0')
        self.first_input_flag = True
        # self.lbl_buffer.setText('')

    # Backspace 버튼을 눌렀을 때
    def btn_back_clicked_slot(self):
        text = self.lbl_result.text()
        self.first_input_flag = False

        if self.opcode == '=':
            self.opcode = ''

        if len(text) == 1 or text == 'infinity':
            self.lbl_result.setText("0")
        else:
            self.lbl_result.setText(text[:len(text) - 1])

    # 창 닫기
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, '종료하기', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())  # 이벤트 루프
