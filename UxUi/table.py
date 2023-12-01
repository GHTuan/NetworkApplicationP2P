import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers):
        super(TableModel, self).__init__()
        self._data = data
        self.headers = headers

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)  # Đổi tên hàng thành số (hoặc bất kỳ thứ gì bạn muốn)

        return super().headerData(section, orientation, role)


class TableWindow(QtWidgets.QMainWindow):
    def setHeader(self,header):
        self.headers = header
    def setData(self,data):
        self.data = data
        self.model = TableModel(self.data, self.headers)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
    def __init__(self):
        super().__init__()
        self.data=[[]]
        self.table = QtWidgets.QTableView()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TableWindow()
    window.show()
    sys.exit(app.exec())

