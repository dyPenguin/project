from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QDialog


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("./infoDig.ui", self)
        self.show()
        self.initUI()

        self.set_url()

    def initUI(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)   # 도움말 버튼 제거
        self.btn_ok.clicked.connect(self.close)

    def set_url(self):
        text = '''<a href="https://github.com/dyshim/PyQt5-Apps/tree/main/NotePad" target="_blank">@GitHub</a>'''
        print(text)
        self.lbl_url.setText(text)
        self.lbl_url.setOpenExternalLinks(True)