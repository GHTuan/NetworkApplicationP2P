# Form implementation generated from reading ui file 'pageshare.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from ..backend.Peer import Peer1
class Ui_Sharewindow(object):
    fileName =''
    peer1 = Peer1
    def setupUi(self, Sharewindow):
        Sharewindow.setObjectName("Sharewindow")
        Sharewindow.resize(413, 390)
        Sharewindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.centralwidget = QtWidgets.QWidget(parent=Sharewindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.header_2.setGeometry(QtCore.QRect(20, 40, 381, 51))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(24)
        self.header_2.setFont(font)
        self.header_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.header_2.setObjectName("header_2")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 160, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 160, 221, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.share = QtWidgets.QPushButton(parent=self.centralwidget)
        self.share.setGeometry(QtCore.QRect(180, 210, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.share.setFont(font)
        self.share.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.share.setObjectName("share")
        self.back1 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back1.setGeometry(QtCore.QRect(0, 0, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.back1.setFont(font)
        self.back1.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.back1.setObjectName("back1")
        Sharewindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Sharewindow)
        self.statusbar.setObjectName("statusbar")
        Sharewindow.setStatusBar(self.statusbar)

        self.retranslateUi(Sharewindow)
        QtCore.QMetaObject.connectSlotsByName(Sharewindow)

        #connect function and button
        # self.share.clicked.connect(self.hello)
        self.share.clicked.connect(self.peer1.send_PUBLISH(self,fileName))

    def retranslateUi(self, Sharewindow):
        _translate = QtCore.QCoreApplication.translate
        Sharewindow.setWindowTitle(_translate("Sharewindow", "ShareFile"))
        self.header_2.setText(_translate("Sharewindow", "SHARE FILE APPLICATION"))
        self.label.setText(_translate("Sharewindow", "Enter your file:"))
        self.share.setText(_translate("Sharewindow", "SHARE"))
        self.back1.setText(_translate("Sharewindow", "BACK"))
    def hello(self):
        global fileName
        fileName = self.lineEdit.text()
        print("hello world ", fileName)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Sharewindow = QtWidgets.QMainWindow()
    ui = Ui_Sharewindow()
    ui.setupUi(Sharewindow)
    Sharewindow.show()
    sys.exit(app.exec())
