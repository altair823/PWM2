# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\FindIDWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IDFindWindow(object):
    def setupUi(self, IDFindWindow):
        IDFindWindow.setObjectName("IDFindWindow")
        IDFindWindow.resize(387, 411)
        self.gridLayout = QtWidgets.QGridLayout(IDFindWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetIDs = QtWidgets.QListWidget(IDFindWindow)
        self.listWidgetIDs.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetIDs.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidgetIDs.setObjectName("listWidgetIDs")
        self.gridLayout.addWidget(self.listWidgetIDs, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonSelectID = QtWidgets.QPushButton(IDFindWindow)
        self.pushButtonSelectID.setObjectName("pushButtonSelectID")
        self.horizontalLayout.addWidget(self.pushButtonSelectID)
        self.pushButtonDeleteID = QtWidgets.QPushButton(IDFindWindow)
        self.pushButtonDeleteID.setObjectName("pushButtonDeleteID")
        self.horizontalLayout.addWidget(self.pushButtonDeleteID)
        self.pushButtonClose = QtWidgets.QPushButton(IDFindWindow)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(IDFindWindow)
        QtCore.QMetaObject.connectSlotsByName(IDFindWindow)

    def retranslateUi(self, IDFindWindow):
        _translate = QtCore.QCoreApplication.translate
        IDFindWindow.setWindowTitle(_translate("IDFindWindow", "Stored IDs"))
        self.pushButtonSelectID.setText(_translate("IDFindWindow", "선택"))
        self.pushButtonDeleteID.setText(_translate("IDFindWindow", "삭제"))
        self.pushButtonClose.setText(_translate("IDFindWindow", "닫기"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IDFindWindow = QtWidgets.QDialog()
    ui = Ui_IDFindWindow()
    ui.setupUi(IDFindWindow)
    IDFindWindow.show()
    sys.exit(app.exec_())
