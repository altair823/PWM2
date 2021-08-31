'''
 사용자에게서 키를 입력받고 이를 사용하여 특정 사이트, 특정 아이디에 대응하는 비밀번호를 생성하는 프로그램이다.
'''
import os

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.MainWindow_ui import Ui_PWMMainWindow
from add_site_window import AddSiteWindow
from find_ID_window import FindIDWIndow
from input_key_window import InputKeyWindow
from otp_scan_window import OTPScanWindow
from sys import exit
from database import Database
from generator import Generator
from security.otp import OTP


class MainWindow(QMainWindow, Ui_PWMMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.database = Database('PW.json')
        self.isCreateInitial = False
        otp = OTP('PWM2')
        otp.makeCredential()
        try:
            # DB를 로드한다.
            self.database.loadFile()
        except FileNotFoundError:
            # 파일이 없다면 프로그램을 처음 키는 것으로 간주한다.
            otp.saveCredentialIMG('Credential.png')
            otpScanWindow = OTPScanWindow(self, 'Credential.png')
            os.remove('Credential.png')
            otpScanWindow.exec_()

        # 사용자의 복호화 키, OTP 를 입력받고 DB와 검증한다.
        while True:
            inputKeyWindow = InputKeyWindow(self)
            inputKeyWindow.exec_()
            if inputKeyWindow.quitFlag is True:
                exit()
            key = inputKeyWindow.key
            inputOTP = inputKeyWindow.otp
            try:
                self.database.verifyPW(str(key))
            except Exception as e:
                QMessageBox.warning(self, '경고', '잘못된 복호화 키 입니다!')
                print(e)
                continue
            try:
                otp.verifyOTP(inputOTP)
            except KeyError:
                QMessageBox.warning(self, '경고', '잘못된 OTP 입니다!')
                continue
            break


        # DB에서 로드한 데이터를 GUI에 표시한다.
        for item in self.database.getSiteList():
            self.comboBoxSiteList.addItem(item)

        self.pushButtonAddSite.clicked.connect(self.addSite)
        self.pushButtonDeleteSite.clicked.connect(self.delSite)

        self.pushButtonMakePW.clicked.connect(self.makePW)
        self.lineEditID.returnPressed.connect(self.makePW)

        self.pushButtonSavePW.clicked.connect(self.savePW)

        self.pushButtonFindID.clicked.connect(self.findID)

        self.optionCollisionFlag = False
        self.checkBoxIsUpperOnly.clicked.connect(self.optionCollision)
        self.checkBoxIsLowerOnly.clicked.connect(self.optionCollision)

        self.pushButtonMakePW.setDisabled(True)
        self.lineEditID.textChanged.connect(self.checkPWMakeButton)
        self.comboBoxSiteList.currentIndexChanged.connect(self.checkPWMakeButton)
        self.lineEditID.textChanged.connect(self.lineEditPW.clear)
        self.comboBoxSiteList.currentIndexChanged.connect(self.lineEditPW.clear)
        self.comboBoxSiteList.currentIndexChanged.connect(self.lineEditID.clear)

    def addSite(self):
        while True:
            addSiteWindow = AddSiteWindow(self)
            addSiteWindow.exec_()
            if addSiteWindow.newSiteName is not None:
                try:
                    self.database.addSite(addSiteWindow.newSiteName)
                except AttributeError:
                    QMessageBox.information(self, 'Info', '이미 존재하는 사이트입니다.')
                    continue
                self.comboBoxSiteList.addItem(addSiteWindow.newSiteName)
                self.comboBoxSiteList.setCurrentText(addSiteWindow.newSiteName)
                break
            else:
                break

    def delSite(self):
        try:
            self.comboBoxSiteList.removeItem(self.comboBoxSiteList.currentIndex())
            self.database.delSite(self.comboBoxSiteList.currentText())
        except AttributeError:
            QMessageBox.information(self, 'Info', '이미 존재하지 않는 사이트 입니다.')

    def optionCollision(self):
        if self.checkBoxIsUpperOnly.isChecked() is True and self.checkBoxIsLowerOnly.isChecked() is True:
            QMessageBox.information(self, 'Info', '소문자와 대문자를 동시에 제외할 수 없습니다.')
            self.checkBoxIsUpperOnly.setChecked(False)
            self.checkBoxIsLowerOnly.setChecked(False)
            self.optionCollisionFlag = True
        else:
            self.optionCollisionFlag = False

    def makePW(self):
        if self.comboBoxSiteList.currentText() == '' or self.lineEditID.text() == '':
            QMessageBox.information(self, 'info', '사이트와 아이디를 올바르게 입력하세요')
        elif self.optionCollisionFlag is True:
            return
        else:
            # 패스워드를 생성한다.
            generator = Generator(
                self.spinBox.value(),
                isSpecialCharInclude=self.checkBoxIsSpecial.isChecked(),
                isNumInclude=self.checkBoxIsNum.isChecked(),
                isUpperOnly=self.checkBoxIsUpperOnly.isChecked(),
                isLowerOnly=self.checkBoxIsLowerOnly.isChecked(),
                isSimilarNotInclude=self.checkBoxIsExcludeSimilar.isChecked())
            PW = generator.makePW()
            self.lineEditPW.setText(PW)

    def savePW(self):
        self.database.addID(self.comboBoxSiteList.currentText(), self.lineEditID.text())
        self.database.addPW(self.comboBoxSiteList.currentText(), self.lineEditID.text(), self.lineEditPW.text())
        QMessageBox.information(self, 'Info', '비밀번호가 저장되었습니다.')
        self.pushButtonMakePW.setDisabled(True)

    def findID(self):
        IDList = []
        if self.comboBoxSiteList.currentText() != '':
            IDList = self.database.getIDList(self.comboBoxSiteList.currentText())
        findIDWIndow = FindIDWIndow(self, IDList)
        findIDWIndow.exec_()
        if findIDWIndow.selectedID != '':
            self.lineEditID.setText(findIDWIndow.selectedID)
            self.lineEditPW.setText(self.database.getPW(self.comboBoxSiteList.currentText(), self.lineEditID.text()))
        if findIDWIndow.toRemoveID != '':
            self.database.delID(self.comboBoxSiteList.currentText(), findIDWIndow.toRemoveID)
        self.checkPWMakeButton()

    def checkPWMakeButton(self):
        if self.comboBoxSiteList.currentText() == '':
            self.pushButtonMakePW.setDisabled(True)
        elif self.database.findSiteID(self.comboBoxSiteList.currentText(), self.lineEditID.text()) is False:
            self.pushButtonMakePW.setEnabled(True)
        else:
            self.pushButtonMakePW.setDisabled(True)

    def closeEvent(self, event):
        self.database.saveFile()
        try:
            #BD(self.key, 'PW.json')
            pass
        except Exception:
            pass



