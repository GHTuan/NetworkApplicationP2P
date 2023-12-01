from PyQt6 import QtGui,QtWidgets, QtCore
import sys
import home, pageshare, pagedown, table, login_page,connect_server
sys.path.append(r".\..")
sys.path.append(r".")
from backend.Peer import Peer

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

table_window = table.TableWindow()

def loginUi():
    global ui
    ui = login_page.Ui_login()
    ui.setupUi(MainWindow)
    ui.loginButton.clicked.connect(LoginClick)
    MainWindow.show()            

def LoginClick():
    # ui from loginUi
    
    username = ui.username_input.text()
    password = ui.password_input.text()
    if p.login(username,password) == "Login in success":
        homeUi()
    else:          
        print("Login Fail! Login again!")

    

def homeUi():
    global ui
    ui = home.Ui_P2P_APP()
    ui.setupUi(MainWindow)
    ui.download.clicked.connect(pagedownUi)
    ui.sharefile.clicked.connect(ShareUi)
    ui.disconect.clicked.connect(DisconnectClick)
    MainWindow.show()
    
def DisconnectClick():
    # ui from homeUi
    p.OFF()
    sys.exit(app.exec())
    
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
    table_window.setHeader(["IP","Port", "Owner", "FileName"])
    
    if result != []:
        table_window.setData(result)    

    table_window.show()
    
def ConnectWindow():
    global ui
    ui = connect_server.Ui_Connect_server()
    ui.setupUi(MainWindow)
    ui.connect_server_btn.clicked.connect(ConnectClick)
    MainWindow.show()

def ConnectClick():
    ip = ui.username_input.text()
    port =  ui.password_input.text()
    if ip=="" or port =="" or ip=="Enter IP of server" or port=="Enter Port of server":
        #use default host
        p.setServerHost()
    else:
        p.setServerHost(ip,int(port))
    r = p.connect_To_MainServer()
    if (r == "Connection establishes"): 
        loginUi()
    else:
        pass
    
   
        
#runapp

p = Peer()
ConnectWindow()
sys.exit(app.exec())