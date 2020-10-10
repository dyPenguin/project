import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('./calculator.ui')[0]  #XML -> CLASS 타입 으로 바꿔줌.

class Exam(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.first_input_flag = True #첫번째 입력 인지 확인하는 변수
        self.setupUi(self)
        self.initUI()
        self.btn_all_clear_clicked_slot()
        self.opcode = ''
        self.buffer = self.lbl_buffer.text()
        self.lst_buffer = []

    def initUI(self):
        self.btn_1.clicked.connect(self.btn_number_clicked_process)
        self.btn_2.clicked.connect(self.btn_number_clicked_process)
        self.btn_3.clicked.connect(self.btn_number_clicked_process)
        self.btn_4.clicked.connect(self.btn_number_clicked_process)
        self.btn_5.clicked.connect(self.btn_number_clicked_process)
        self.btn_6.clicked.connect(self.btn_number_clicked_process)
        self.btn_7.clicked.connect(self.btn_number_clicked_process)
        self.btn_8.clicked.connect(self.btn_number_clicked_process)
        self.btn_9.clicked.connect(self.btn_number_clicked_process)
        self.btn_0.clicked.connect(self.btn_number_clicked_process)
        self.btn_add.clicked.connect(self.btn_opcode_clicked_process)
        self.btn_sub.clicked.connect(self.btn_opcode_clicked_process)
        self.btn_mul.clicked.connect(self.btn_opcode_clicked_process)
        self.btn_div.clicked.connect(self.btn_opcode_clicked_process)
        self.btn_equal.clicked.connect(self.btn_opcode_clicked_process)
        self.btn_all_clear.clicked.connect(self.btn_all_clear_clicked_slot)
        self.btn_clear.clicked.connect(self.btn_clear_clicked_slot)
        self.btn_back.clicked.connect(self.btn_back_clicked_slot)
        self.btn_comma.clicked.connect(self.btn_comma_clicked_slot)

    """
    *** Tip. ***
    - bool 타입 확인 함수는 관습적으로 이름 붙일 때 is_를 붙여줌.
    """

    # 숫자 버튼을 눌렀을 때
    def btn_number_clicked_process(self):
        self.btn_disable_process(True)

        if self.lbl_result.text() == '0':
            self.first_input_flag = True

        if self.first_input_flag:
            self.first_input_flag = False
            self.lbl_result.setText('')

        if self.opcode == '=' :
            self.lbl_buffer.clear()
            self.lst_buffer = []
            self.lbl_result.setText('')
            self.opcode = ''

        # 버튼으로 입력된 값을 변수에 저장.
        str_sender = self.sender().text()
        str_lbl = self.lbl_result.text()
        self.lbl_result.setText(str_lbl + str_sender)

    # . 을 입력했을 경우
    def btn_comma_clicked_slot(self):
        if self.first_input_flag:
            self.lbl_result.setText('0')

        self.first_input_flag = False
        str_lbl = self.lbl_result.text()

        if '.' not in self.lbl_result.text() :
            self.lbl_result.setText(str_lbl + '.')

    # 계산 수식을 라벨에 출력
    def lbl_buffer_process(self, number, opcode):
        self.lst_buffer.append(str(number))
        self.lst_buffer.append(opcode)
        lbl_buffer = ''
        result = ''

        for buffer in self.lst_buffer:
            lbl_buffer += buffer + ' '
        self.lbl_buffer.setText(lbl_buffer)

        if self.lst_buffer[-1] == '=':
            self.lst_buffer.clear()
            result = self.lbl_result.text()
        return result

    # infinity 값일 때 버튼 비활성화
    def btn_disable_process(self, bool):
        self.btn_add.setEnabled(bool)
        self.btn_sub.setEnabled(bool)
        self.btn_mul.setEnabled(bool)
        self.btn_div.setEnabled(bool)
        self.btn_comma.setEnabled(bool)
        self.btn_back.setEnabled(bool)

    # 연산자를 눌렀을 때
    def btn_opcode_clicked_process(self):
        # 연속으로 연산자를 두번 눌렀을 때
        if self.first_input_flag :
            self.opcode = self.sender().text()
        else:
            self.first_input_flag = True #첫번째 숫자 입력이 끝났기 때문에 flag 값을 true 로 바꿔줌.
            self.number = float(self.lbl_result.text())
            self.lbl_result.setText(str(self.number))
            if self.opcode != '':
                self.calculate()
            self.result = float(self.lbl_result.text())
            print(self.result)

            # infinity 값일 경우 더이상 계산할수 없게 버튼을 비활성화
            if self.result == float('inf'):
                print('error!!')
                self.lbl_result.setText('infinity')
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
                self.result = 'infinity'
            else:
                self.result = self.result / self.number
        elif self.opcode == '=':
            self.result = float(self.lbl_result.text())
            self.lst_buffer = []
        self.lbl_result.setText(str(self.result))
        self.lbl_buffer.clear()

    # '=' 버튼을 눌렀을 때
    def btn_equal_clicked_process(self):
        self.first_input_flag = True
        self.calculate()
        self.opcode = '=' # '=' 를 눌렀을때 결과값이 출력 되도록 하기 위해선 op연산자를 초기화 해야 함.

    # AC 버튼을 눌렀을 때
    def btn_all_clear_clicked_slot(self):
        self.number = 0
        self.opcode = '='
        self.lbl_result.setText('0')
        self.lbl_buffer.setText('')
        self.first_input_flag = True

    # C 버튼을 눌렀을 때
    def btn_clear_clicked_slot(self):
        self.lbl_result.setText('0')
        self.first_input_flag = True
        #self.lbl_buffer.setText('')

    # Backspace를 눌렀을 때
    def btn_back_clicked_slot(self):
        str_lbl = self.lbl_result.text()
        result_len = len(str_lbl)
        self.first_input_flag = False

        if result_len == 1 or str_lbl == 'infinity':
            str_lbl = "0"
            self.lbl_result.setText(str_lbl)
        else :
            str_lbl = str_lbl[:result_len-1]
            self.lbl_result.setText(str_lbl)

    # 창 닫기
    def closeEvent(self, QCloseEvent) :
        pass
        ans = QMessageBox.question(self, '종료하기', '종료하시겠습니까?',QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())   # 이벤트 루프
