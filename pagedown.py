# Form implementation generated from reading ui file 'pagedown.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Download(object):
    def setupUi(self, Download):
        Download.setObjectName("Download")
        Download.resize(407, 391)
        Download.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.centralwidget = QtWidgets.QWidget(parent=Download)
        self.centralwidget.setObjectName("centralwidget")
        self.header_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.header_2.setGeometry(QtCore.QRect(20, 50, 381, 51))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(24)
        self.header_2.setFont(font)
        self.header_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.header_2.setObjectName("header_2")
        self.back2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back2.setGeometry(QtCore.QRect(10, 340, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.back2.setFont(font)
        self.back2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.back2.setObjectName("back2")
        self.disconect = QtWidgets.QPushButton(parent=self.centralwidget)
        self.disconect.setGeometry(QtCore.QRect(150, 340, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.disconect.setFont(font)
        self.disconect.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.disconect.setObjectName("disconect")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 140, 411, 171))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 110, 47, 14))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        Download.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Download)
        self.statusbar.setObjectName("statusbar")
        Download.setStatusBar(self.statusbar)

        self.retranslateUi(Download)
        QtCore.QMetaObject.connectSlotsByName(Download)

    def retranslateUi(self, Download):
        _translate = QtCore.QCoreApplication.translate
        Download.setWindowTitle(_translate("Download", "MainWindow"))
        self.header_2.setText(_translate("Download", "SHARE FILE APPLICATION"))
        self.back2.setText(_translate("Download", "BACK"))
        self.disconect.setText(_translate("Download", "DISCONECT"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("Download", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Download", "Name file"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Download", "Owner"))
        self.label.setText(_translate("Download", "List file"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Download = QtWidgets.QMainWindow()
    ui = Ui_Download()
    ui.setupUi(Download)
    Download.show()
    sys.exit(app.exec())
