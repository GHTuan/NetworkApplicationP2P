from PyQt6 import QtGui,QtWidgets, QtCore
import sys
import home, pageshare, pagedown, table, login_page
sys.path.append(r".\..")
sys.path.append(r".")
from backend.Peer import Peer

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
table_window = table.TableWindow()

USER = "123"
PASS = "123"

def loginUi():
    global ui
    ui = login_page.Ui_login()
    ui.setupUi(MainWindow)
    username = ui.username_input.text()
    passwork = ui.password_input.text()
    notLog = True #chưa đăng nhập =true
    while notLog:
        if p.login(username,passwork) == "Login in success":
            ui.loginButton.clicked.connect(homeUi)
            notLog = False
        else:
            notLog = True   
            print("Login Fail! Login again!") 
    MainWindow.show()            

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
    ui.search_btn.clicked.connect(TableUi)
    ui.fetch_btn.clicked.connect(FetchClicked)
    MainWindow.show()

def FetchClicked():
    # ui from pagedownUi
    ip = ui.IP_text_box.text()
    port = int(ui.Port_text_box.text())
    file_name = ui.filename_text_box.text()
    p.fetch((ip,port),file_name)
    

def ShareUi():
    global ui
    ui = pageshare.Ui_Sharewindow()
    ui.setupUi(MainWindow)
    ui.share.clicked.connect(ShareClicked)
    ui.back1.clicked.connect(homeUi)
    MainWindow.show()

def ShareClicked():
    #ui from ShareUi
    filename = ui.lineEdit.text()
    p.send_PUBLISH(filename)

def TableUi():
    # ui from pagedownUi
    filter = ui.search_box.text()
    data = p.send_DISCOVER(filter) 
    result = []
    
    for (ip, port), (name, files) in data.items():
        for file in files:
            result.append([ip, port , name, file])
        
    if result != []:
        table_window.setData(result)    
        
    table_window.show()
    
#runapp

p = Peer()
# p.login("123","123")
loginUi()
sys.exit(app.exec())