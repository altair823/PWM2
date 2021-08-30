from ui.FindIDWindow_ui import Ui_IDFindWindow
from PyQt5.QtWidgets import QDialog


class FindIDWIndow(QDialog, Ui_IDFindWindow):
    def __init__(self, parent, IDList):
        super().__init__(parent)
        self.setupUi(self)
        for i in IDList:
            self.listWidgetIDs.addItem(i)
        self.selectedID = ''
        self.toRemoveID = ''
        self.pushButtonSelectID.clicked.connect(self.selectID)
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonDeleteID.clicked.connect(self.deleteID)

    def selectID(self):
        if self.listWidgetIDs.currentItem():
            self.selectedID = self.listWidgetIDs.currentItem().text()
            self.close()

    def deleteID(self):
        if self.listWidgetIDs.currentItem():
            self.toRemoveID = self.listWidgetIDs.currentItem().text()
            self.listWidgetIDs.takeItem(self.listWidgetIDs.currentRow())
