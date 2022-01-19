from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore


class FindDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("./findDig.ui", self)
        self.show()

        self.initUI()
        self.parent = parent
        self.cursor = parent.pe.textCursor()

    def initUI(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # 도움말 버튼 제거

        self.btn_findNext.clicked.connect(self.find_next)
        self.btn_cancle.clicked.connect(self.close)

    def keyReleaseEvent(self, event):
        if self.LineEdit.text():
            self.btn_findNext.setEnabled(True)
        else:
            self.btn_findNext.setEnabled(False)

    def find_next(self):
        pattern = self.LineEdit.text()  # 찾을 내용
        text = self.parent.pe.toPlainText()  # 본문 내용
        reg = QtCore.QRegExp(pattern)  # 정규 표현식

        # 대/소문자 구분
        if self.chkbx_caseSensitive.isChecked():
            cs = Qt.CaseSensitive
        else:
            cs = Qt.CaseInsensitive
        reg.setCaseSensitivity(cs)

        self.cursor = self.parent.pe.textCursor()
        pos = self.cursor.position()

        '''
        indexIn(Index 검색 기능)
        - 커서 위치(pos)에서부터 본문(text)과 일치하는 패턴값의 위치 반환
        '''

        # 검색 방향 선택
        if self.rdo_up.isChecked():
            print("up")
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)  # 역방향 검색
        else:
            print("down")
            index = reg.indexIn(text, pos)  # 정방향 검색

        if (index != -1) & (pos > -1):  # 검색 결과가 존재 ○
            self.set_cursor(index, len(pattern) + index)
        else:
            QMessageBox.information(self, "메모장", f'''{pattern}을(를) 찾을 수 없습니다.''')

    def set_cursor(self, start, end):
        # print(self.cursor.selectionStart(), self.cursor.selectionEnd())

        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.parent.pe.setTextCursor(self.cursor)


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("./infoDig.ui", self)
        self.show()
        self.initUI()

        self.set_url()

    def initUI(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # 도움말 버튼 제거
        self.btn_ok.clicked.connect(self.close)

    def set_url(self):
        text = '''<a href="https://github.com/dyshim/PyQt5-Apps/tree/main/NotePad" target="_blank">@GitHub</a>'''
        print(text)
        self.lbl_url.setText(text)
        self.lbl_url.setOpenExternalLinks(True)
