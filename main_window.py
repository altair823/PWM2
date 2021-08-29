'''
 사용자에게서 키를 입력받고 이를 사용하여 특정 사이트, 특정 아이디에 대응하는 비밀번호를 생성하는 프로그램이다.
'''
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.MainWindow_ui import Ui_PWMMainWindow
from add_site_window import AddSiteWindow
from find_ID_window import FindIDWIndow
from input_key_window import InputKeyWindow
from sys import exit
from encryption import Encryption
from database import Database
from generator import Generator


class MainWindow(QMainWindow, Ui_PWMMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.cryptoMachine = Encryption()
        self.database = Database('PW.json')
        self.isCreateInitial = False
        try:
            # DB를 로드한다.
            self.database.loadFile()
        except FileNotFoundError:
            # 파일이 없다면 프로그램을 처음 키는 것으로 간주한다.
            self.isCreateInitial = True

        # 사용자의 복호화 키를 입력받고 DB와 검증한다.
        while True:
            inputKeyWindow = InputKeyWindow(self)
            inputKeyWindow.exec_()
            if inputKeyWindow.quitFlag is True:
                exit()
            self.PW = inputKeyWindow.key
            try:
                self.cryptoMachine.verifyPW(str(self.PW), self.database.hashedPW, self.database.salt,
                                            isCreateInitial=self.isCreateInitial)
            except Exception as e:
                QMessageBox.warning(self, '경고', '잘못된 복호화 키 입니다!')
                print(e)
                continue
            break

        self.generator = Generator(20)

        # DB에서 로드한 데이터를 GUI에 표시한다.
        for item in self.database.PWs:
            self.comboBoxSiteList.addItem(item)

        self.pushButtonAddSite.clicked.connect(self.addSite)
        self.pushButtonDeleteSite.clicked.connect(self.delSite)

        self.pushButtonMakePW.clicked.connect(self.makePW)
        self.lineEditID.returnPressed.connect(self.makePW)

        self.pushButtonFindID.clicked.connect(self.findID)

    def addSite(self):
        addSiteWindow = AddSiteWindow(self)
        addSiteWindow.exec_()
        if addSiteWindow.newSiteName is not None:
            self.comboBoxSiteList.addItem(addSiteWindow.newSiteName)
            self.comboBoxSiteList.setCurrentText(addSiteWindow.newSiteName)

    def delSite(self):
        self.database.delSite(self.cryptoMachine.encryptPW(self.comboBoxSiteList.currentText()))
        self.comboBoxSiteList.removeItem(self.comboBoxSiteList.currentIndex())

    def makePW(self):
        if self.comboBoxSiteList.currentText() == '' or self.lineEditID.text() == '':
            QMessageBox.information(self, 'info', '사이트와 아이디를 올바르게 입력하세요')
        else:
            # 패스워드를 생성한다.
            PW = self.generator.makePW()
            currentHashedSitename = self.cryptoMachine.hashing(self.comboBoxSiteList.currentText())
            self.database.PWs[currentHashedSitename] = {self.lineEditID.text(): self.cryptoMachine.encryptPW(PW)}
            self.lineEditPW.setText(PW)

    def findID(self):
        decryptedIDList = []
        if self.cryptoMachine.hashing(self.comboBoxSiteList.currentText()) in self.database.PWs:
            encryptedIDList = list(self.cryptoMachine.PWs[self.comboBoxSiteList.currentText()].keys())
            for i in encryptedIDList:
                decryptedIDList.append(self.cryptoMachine.fernet.decrypt(i.encode()).decode())
        findIDWIndow = FindIDWIndow(self, decryptedIDList)
        findIDWIndow.exec_()
        if findIDWIndow.selectedID != '':
            self.lineEditID.setText(findIDWIndow.selectedID)
            self.makePW()

    def closeEvent(self, event):
        self.database.saveFile()
        try:
            #BD(self.key, 'PW.json')
            pass
        except Exception:
            pass



