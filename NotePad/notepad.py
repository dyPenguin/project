import os.path
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from subForm import AboutDialog, FindDialog
from datetime import datetime

form_window = uic.loadUiType('./notepad.ui')[0]


class Form(QMainWindow, form_window):
    def __init__(self):
        super(Form, self).__init__()
        self.setupUi(self)
        self.initUI()

        self.path = "제목 없음"
        self.isOpened = False  # 파일 오픈 상태 확인
        self.windows = list()

        # Update the title
        self.update_title(self.path)

    def initUI(self):
        # File menu
        self.action_win.triggered.connect(self.add_window)
        self.action_open.triggered.connect(self.file_open)
        self.action_save.triggered.connect(self.file_save)
        self.action_save_as.triggered.connect(self.file_save_as)
        self.action_new.triggered.connect(self.file_new)
        self.action_close.triggered.connect(self.close)

        # Edit menu
        self.action_undo.triggered.connect(self.pe.undo)
        self.action_redo.triggered.connect(self.pe.redo)
        self.action_all_select.triggered.connect(self.pe.selectAll)
        self.action_cut.triggered.connect(self.pe.cut)
        self.action_copy.triggered.connect(self.pe.copy)
        self.action_paste.triggered.connect(self.pe.paste)
        self.action_del.triggered.connect(self.pe.cut)
        self.action_find.triggered.connect(self.find_word)
        self.action_datetime.triggered.connect(self.insert_datetime)

        # Option menu
        self.action_font.triggered.connect(self.set_font)

        self.action_about.triggered.connect(self.form_info)

        self.pe.textChanged.connect(lambda: self.update_title(self.path))

    def update_title(self, title):
        # print("== Update Title Execute ==")
        if title != "제목 없음":
            title = os.path.splitext(os.path.basename(self.path))[0]

        if self.isTextChanged():
            title = "*" + title

        self.setWindowTitle(f"{title} - Penguin's 메모장")

    def add_window(self):   # 새 창(W)
        # print("== Add window Execute ==")
        new_win = Form()
        self.windows.append(new_win)
        new_win.show()

    def file_open(self):  # 열기(O)
        # print("== File Open Execute ==")
        if self.isTextChanged():
            # 내용이 변경된 상태에서 취소 버튼 클릭 시
            if self.answer_to_save() == 2:
                return 0

        f_name = QFileDialog.getOpenFileName(self, filter="텍스트 문서(*.txt);;모든 파일(*.*)")

        if f_name[0]:
            with open(f_name[0], encoding='UTF-8') as f:
                text = f.read()

            self.path = f_name[0]
            self.isOpened = True
            self.pe.setPlainText(text)

            # Update the title
            self.update_title(self.path)

    def file_save(self):  # 저장(S)
        # print("== File Save Execute ==")
        if self.isOpened:
            self._save_to_path(self.path)

            # Update the title
            self.update_title(self.path)
        else:
            if self.file_save_as():
                return -1

    def file_save_as(self):  # 다른 이름으로 저장(A)
        # print("== File Save As Execute ==")
        f_name = QFileDialog.getSaveFileName(self, filter="텍스트 문서(*.txt);;모든 파일(*.*)")

        if f_name[0]:
            self.path = f_name[0]
            self._save_to_path(self.path)
            self.isOpened = True

            # Update the title
            self.update_title(self.path)
        else:
            return -1

    def _save_to_path(self, f_path):
        text = self.pe.toPlainText()
        with open(f_path, 'w', encoding='UTF-8') as f:
            f.write(text)

    def file_new(self):  # 새로 만들기(N)
        # print("== File Mew Execute ==")
        if self.isTextChanged():
            # 취소 버튼 클릭 시
            if self.answer_to_save() == 2:
                return 0

        self.isOpened = False
        self.pe.clear()
        self.update_title("제목 없음")

    def isTextChanged(self):
        current_text = self.pe.toPlainText()

        if self.isOpened:
            # 기존 파일에 저장된 데이터
            if self.path:
                with open(self.path, encoding='UTF-8') as f:
                    text = f.read()
                if current_text != text:
                    return True
        else:
            # 열린 파일은 없는데 작성한 내용이 있는 경우
            if current_text:
                return True

        return False

    def answer_to_save(self):
        # 사용자에게 저장 여부 요청
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Penguin's 메모장")
        msgBox.setText(f"변경 내용을 {self.path}에 저장하시겠습니까?")
        msgBox.addButton("저장", QMessageBox.YesRole)  # 0
        msgBox.addButton("저장 안 함", QMessageBox.NoRole)  # 1
        msgBox.addButton("취소", QMessageBox.RejectRole)  # 2
        ans = msgBox.exec_()

        if ans == 0:
            if self.file_save():
                return 2   # 저장 취소 시
        else:
            return ans

    def set_font(self):  # 글꼴 설정
        font = QFontDialog.getFont(self.font(), self, "글꼴")  # OS 에서 제공
        if font[1]:
            self.pe.setFont(font[0])

    def form_info(self):  # 메모장 정보
        dlg = AboutDialog(self)
        dlg.exec_()

    def closeEvent(self, event):  # 닫기 버튼 눌렀을 때
        # print("== Run close Event ==")
        if self.isTextChanged():
            # 취소 버튼 클릭 시
            if self.answer_to_save() == 2:
                event.ignore()
        else:
            event.accept()

    def find_word(self):   # 찾기(F)
        # print("== Run Find Word Function ==")
        dlg = FindDialog(self)
        dlg.show()

    def insert_datetime(self):   # 시간/날짜
        current_time = datetime.now()
        self.pe.textCursor().insertText(current_time.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    winForm = Form()
    winForm.show()
    sys.exit(app.exec_())  # 이벤트 루프
