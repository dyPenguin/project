import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
from PyQt5 import uic
form_window = uic.loadUiType('./notepad.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self):
        self.open_flag = False  #새 파일인지 여부 확인.
        self.file = ('제목 없음','')    #(경로, 저장 타입)
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setWindowTitle('NotePad - ' + self.file[0])

    def initUI(self):
        self.action_save_as.triggered.connect(self.action_save_as_slot)   #connect(괄호 주의!)
        self.action_save.triggered.connect(self.action_save_slot)
        self.action_open.triggered.connect(self.action_open_slot)
        self.action_font.triggered.connect(self.action_font_slot)
        self.action_close.triggered.connect(self.action_close_slot)
        self.action_cut.triggered.connect(self.action_cut_slot)
        self.action_copy.triggered.connect(self.action_copy_slot)
        self.action_paste.triggered.connect(self.action_paste_slot)
        self.action_del.triggered.connect(self.action_del_slot)
        self.action_undo.triggered.connect(self.action_undo_slot)
        self.action_redo.triggered.connect(self.action_redo_slot)
        self.action_all_select.triggered.connect(self.action_all_select_slot)
        self.action_about.triggered.connect(self.action_about_slot)
        self.action_new.triggered.connect(self.action_new_slot)

    def setTitle(self):
        Title = self.file[0]
        if Title == '' :
            Title = '제목 없음'
        Title = Title.split('/')
        self.setWindowTitle('NotePad - ' + Title[-1])


    """
    *** 파일 저장 함수 ***
    - ① FileDialog 는 운영체제의 종속적임.
    - ② .getSaveFileName은 파일 경로만 return 해줌.
    - ③ with 문을 쓰면 close를 쓰지 않아도 됨.
    - ④ path는 튜플의 형태이기 때문에 인덱스 지정 중요!
    """

    # 다른 이름으로 저장
    def action_save_as_slot(self):
        path = self.file
        self.file = QFileDialog.getSaveFileName(self, "save file", "",
                                          "Text Files(*.txt);;Python Files(*.py);;All Files(*.*)", "") #1, 2 / path 에 튜플 형태의 파일 return.

        if self.file[0] :
            str_write = self.plainTextEdit.toPlainText()    #plainText에 있는 문자열들을 읽어옴
            with open(self.file[0], 'w') as f: #3, 4
                f.write(str_write)
            self.open_flag = True
        else :
            self.file = path
        self.setTitle()
        # print(self.file)
        # print(self.open_flag)

    # 수정 여부 확인
    def is_edited(self):
        str_plain = self.plainTextEdit.toPlainText()
        if self.open_flag :
            with open(self.file[0]) as f:
                str_file = f.read()
            return str_plain != str_file    #다르면(변경 O) True, 같으면(변경 X) False 를 return.
        else :
            return str_plain != ''

    # 저장 여부 확인
    def answer_user(self):
        msg_box = QMessageBox()
        msg_box.setText('변경 내용을 ' + self.file[0] + ' 에 저장하시겠습니까?') #setText 는 + 로 연결.
        msg_box.addButton('저장', QMessageBox.YesRole)  # YesRole 은 0 을 return.
        msg_box.addButton('저장 안함', QMessageBox.NoRole)  # YesRole 은 1 을 return.
        msg_box.addButton('취소', QMessageBox.RejectRole)  # YesRole 은 2 을 return.
        return msg_box.exec_()

    def save_edited(self):
        if self.is_edited() :
            answer = self.answer_user()
            if answer == 0 :
                if self.open_flag :
                    with open(self.file[0], 'w') as f:
                        f.write(self.plainTextEdit.toPlainText())
                else :  #save 창 오픈.
                    self.action_save_as_slot()
            elif answer == 2 :  #취소 버튼 눌렀을 때
                return answer

    # 새로 만들기
    def action_new_slot(self):
        if self.save_edited() != 2 :
            self.plainTextEdit.setPlainText('')
            self.open_flag = False
            self.file = ('제목 없음', '')
            self.setTitle()

    """
    *** 파일 열기 ***
    ① getOpenFileName( ,제목, 경로(생략하면 현 dir 보여줌), 필터링->.txt 파일만 보여줌. ;; 으로 구분.)
    """

    # 파일 열기
    def action_open_slot(self):
        self.file = QFileDialog.getOpenFileName(self, "open file", "",
                                           "Text Files(*.txt);;Python Files(*.py);;All Files(*.*)", "")
        if self.file[0] :
            with open(self.file[0], 'r') as f: #'r' 은 생략 가능.
                str_read = f.read()
            self.plainTextEdit.setPlainText(str_read)   #plainText에 있는 문자열들을 메모장에 써줌.
            self.open_flag = True #파일을 열었다는 것을 알리는 변수
        self.setTitle()
    
    """
    *** 글꼴 ***
    ① 글꼴 화면에서 확인 버튼을 누르면 font[1]에 True, 취소 버튼을 누르면 False 반환.
    """
    def action_font_slot(self): #서식-글꼴
        font = QFontDialog.getFont()   #운영체제에서 제공. Font를 return.
        if font[1] : # True 이면 폰트값을 변경 해줌.
            self.plainTextEdit.setFont(font[0])

    def action_close_slot(self): #끝내기
        QCoreApplication.instance().quit()
        print('종료')

    def action_save_slot(self): #파일 저장
        # print('OK')
        if self.open_flag :
            str_write = self.plainTextEdit.toPlainText()
            with open(self.file[0], 'w') as f:
                f.write(str_write)
        else:
            self.action_save_as_slot()

        # print(self.open_flag)
        # print(self.file)

    def action_cut_slot(self):  #잘라내기
        self.plainTextEdit.cut()

    def action_copy_slot(self): #복사
        self.plainTextEdit.copy()

    def action_paste_slot(self): #붙여넣기
        self.plainTextEdit.paste()

    def action_del_slot(self): #삭제
        self.plainTextEdit.cut()

    def action_undo_slot(self): #실행 취소
        self.plainTextEdit.undo()

    def action_redo_slot(self): #다시 실행
        self.plainTextEdit.redo()

    def action_all_select_slot(self):   #모두 선택
        self.plainTextEdit.selectAll()
    """
    *** 메모장 정보 ***
    .about(self, 제목, 내용)
    """
    def action_about_slot(self): #메모장 정보
        QMessageBox.about(self, 'PyQt Pad','''
        만든이 : ABC Lab
        버전 정보 : version 1.0.0
        ''')

    def closeEvent(self, QCloseEvent):  #닫기 버튼 눌렀을 때
        save = self.save_edited()
        #print(1)
        if save == 2 :
            QCloseEvent.ignore()
        # print(self.file)


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())   # 이벤트 루프