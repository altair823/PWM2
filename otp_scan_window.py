from PyQt5.QtGui import QPixmap
from ui.OTPScanWindow_ui import Ui_OTPScanWindow
from PyQt5.QtWidgets import QDialog


class OTPScanWindow(Ui_OTPScanWindow, QDialog):
    def __init__(self, parent, fileName='Credential.png'):
        super().__init__(parent)
        self.setupUi(self)
        self.pix = QPixmap()
        self.pix.load(fileName)
        self.labelQR.setPixmap(self.pix)
