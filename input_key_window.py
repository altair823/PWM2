import sys
from ui.InputKeyWindow_ui import Ui_DialogInputKeyWindow
from PyQt5.QtWidgets import QDialog


class InputKeyWindow(QDialog, Ui_DialogInputKeyWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.quitFlag = False
        self.buttonBox.accepted.connect(self.inputKey)

    def inputKey(self):
        self.key = self.lineEditKey.text()
        self.otp = self.lineEditOTP.text()

    def closeEvent(self, event):
        self.quitFlag = True
        sys.exit()



