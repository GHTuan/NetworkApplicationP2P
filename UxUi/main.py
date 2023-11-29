from PyQt6 import QtGui,QtWidgets, QtCore
import sys
sys.path.append(r'.\..\NetworkApplicationP2P')
import home, pageshare, pagedown

from backend.Peer import Peer

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

def homeUi():
    global ui
    ui = home.Ui_P2P_APP()
    ui.setupUi(MainWindow)
    ui.download.clicked.connect(pagedownUi)
    ui.sharefile.clicked.connect(ShareUi)
    MainWindow.show()

def pagedownUi():
    global ui
    ui = pagedown.Ui_Download()
    ui.setupUi(MainWindow)
    ui.back2.clicked.connect(homeUi)
    ui.fetch_btn.clicked(p.fetch(ui.IP_text_box,ui.Port_text_box,ui.filename_text_box))
    MainWindow.show()

def ShareUi():
    global ui
    ui = pageshare.Ui_Sharewindow()
    ui.setupUi(MainWindow)
    ui.back1.clicked.connect(homeUi)
    MainWindow.show()


#runapp
p = Peer()
homeUi()
sys.exit(app.exec())