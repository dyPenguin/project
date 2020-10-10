import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('./calculator.ui')[0]  #XML -> CLASS 타입 으로 바꿔줌.

# stack class
class stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def isEmpty(self):
        return not self.items

class Exam(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.first_input_flag = True  # 첫번째 입력 값인지 확인하는 변수
        self.opcode = ''
        self.stk = stack() # lbl_buffer 에 출력하기 위한 스택 생성

    def initUI(self):
        self.btn_0.clicked.connect(self.btn_number_clicked)
        self.btn_1.clicked.connect(self.btn_number_clicked)
        self.btn_2.clicked.connect(self.btn_number_clicked)
        self.btn_3.clicked.connect(self.btn_number_clicked)
        self.btn_4.clicked.connect(self.btn_number_clicked)
        self.btn_5.clicked.connect(self.btn_number_clicked)
        self.btn_6.clicked.connect(self.btn_number_clicked)
        self.btn_7.clicked.connect(self.btn_number_clicked)
        self.btn_8.clicked.connect(self.btn_number_clicked)
        self.btn_9.clicked.connect(self.btn_number_clicked)
        self.btn_add.clicked.connect(self.btn_opcode_clicked)
        self.btn_sub.clicked.connect(self.btn_opcode_clicked)
        self.btn_mul.clicked.connect(self.btn_opcode_clicked)
        self.btn_div.clicked.connect(self.btn_opcode_clicked)
        self.btn_equal.clicked.connect(self.btn_opcode_clicked)
        self.btn_all_clear.clicked.connect(self.All_Clear)
        self.btn_clear.clicked.connect(self.Clear)
        self.btn_back.clicked.connect(self.Backspace_clicked)
        self.btn_comma.clicked.connect(self.btn_comma_clicked)

    # 숫자 버튼을 눌렀을 때
    def btn_number_clicked(self):
        self.btn_disable(True) # 버튼 활성화

        # 첫번째 입력값이 0 일때 한번만 출력
        if self.lbl_result.text() == '0':
            self.first_input_flag = True

        if self.first_input_flag:
            self.first_input_flag = False
            self.lbl_result.setText('')

        if self.opcode == '=':
            self.opcode = ''
            self.lbl_result.setText('')
            self.lbl_buffer.clear()
            self.stk.items.clear()

        # 버튼으로 입력된 값을 변수에 저장.
        str_sender = self.sender().text()
        str_lbl = self.lbl_result.text()
        self.lbl_result.setText(str_lbl + str_sender)

    # 연산자 버튼을 눌렀을 때
    def btn_opcode_clicked(self):
        self.number = float(self.lbl_result.text())
        # 연산자를 두번 눌렀을 경우
        if self.first_input_flag:
            self.stk.pop() # 기존 연산자 제거
            self.number = self.stk.pop() # 피연산자 저장
            self.opcode = self.sender().text()
        else:
            self.first_input_flag = True
            self.lbl_result.setText(str(self.number))
            if self.opcode != '':
                self.calculate()
            self.opcode = self.sender().text()
            self.result = float(self.lbl_result.text())
        self.buffer_process(self.number, self.opcode)

    def calculate(self):
        # print('계산 시작!')
        try:
            if self.opcode == '+':
                self.result = self.result + self.number
            elif self.opcode == '-':
                self.result = self.result - self.number
            elif self.opcode == '*':
                self.result = self.result * self.number
            elif self.opcode == '/':
                self.result = self.result / self.number
            elif self.opcode == '=':
                self.result = self.number
        except:
            if ZeroDivisionError:
                self.result = 'infinity'
                self.btn_disable(False)
        self.lbl_result.setText(str(self.result))

    # infinity 값일 때 버튼 비활성화
    def btn_disable(self, bool):
        self.btn_add.setEnabled(bool)
        self.btn_sub.setEnabled(bool)
        self.btn_mul.setEnabled(bool)
        self.btn_div.setEnabled(bool)
        self.btn_comma.setEnabled(bool)
        self.btn_back.setEnabled(bool)
        self.btn_clear.setEnabled(bool)
        self.btn_equal.setEnabled(bool)

    # 계산 수식 출력
    def buffer_process(self, number, opcode):
        self.stk.push(str(number))
        self.stk.push(opcode)
        str_buffer = ''

        for item in self.stk.items:
            str_buffer += ' ' + item
        self.lbl_buffer.setText(str_buffer)
        # print(self.stk.items)
        if self.opcode == '=':
            self.stk.items.clear()
            self.first_input_flag = False

    def All_Clear(self):
        self.btn_disable(True)
        self.number = 0
        self.lbl_result.setText('0')
        self.lbl_buffer.clear()
        self.stk.items.clear()

    def Clear(self):
        self.lbl_result.setText('0')

    def Backspace_clicked(self):
        str_lbl = self.lbl_result.text()
        result_len = len(str_lbl)
        if self.opcode == '=':
            self.opcode = ''

        if result_len == 1 or str_lbl == 'infinity':
            str_lbl = "0"
            self.lbl_result.setText(str_lbl)
        else:
            str_lbl = str_lbl[:result_len-1]
            self.lbl_result.setText(str_lbl)
        print(self.first_input_flag)

    def btn_comma_clicked(self):
        if self.first_input_flag:
            self.lbl_result.setText('0')

        if self.opcode == '=':
            self.opcode = ''

        self.first_input_flag = False
        str_lbl = self.lbl_result.text()
        if '.' not in str_lbl:
            self.lbl_result.setText(str_lbl + '.')

    # 창 닫기
    def closeEvent(self, QCloseEvent) :
        pass
        ans = QMessageBox.question(self, '종료하기', '종료하시겠습니까?',
                                   defaultButton=QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())   # 이벤트 루프