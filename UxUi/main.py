from PyQt6 import QtGui,QtWidgets, QtCore
import sys
import home, pageshare, pagedown, table, login_page,connect_server,AlertWindow
sys.path.append(r".\..")
sys.path.append(r".")
from backend.Peer import Peer

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

table_window = table.TableWindow()
Alert = AlertWindow.Ui_Alert()

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
        Alert.setupUi("Login Fail! Login again!")
        Alert.show()

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
    app.quit()
    
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
    r = "Error" #Place holder
    r = p.fetch((ip,port),file_name)
    Alert.setupUi(r)
    Alert.show()
    
def ShareUi():
    global ui
    ui = pageshare.Ui_Sharewindow()
    ui.setupUi(MainWindow)
    ui.share.clicked.connect(ShareClicked)
    ui.un_share_btn.clicked.connect(UnShareClicked)
    ui.back1.clicked.connect(homeUi)
    MainWindow.show()

def ShareClicked():
    #ui from ShareUi
    filename = ui.lineEdit.text()
    p.send_PUBLISH(filename)
    Alert.setupUi("Your file has been publish\n Check by searching in Download menu")
    Alert.show()
    
def UnShareClicked():
    filename = ui.unshare_box.text()
    p.send_UNPUBLISH(filename)
    Alert.setupUi("Your file has been unpublish\n Check by searching in Download menu")
    Alert.show()
    

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
    else: 
        Alert.setupUi("There is no file being share")
        Alert.show()   

    
    
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
        Alert.setupUi("The server is ofline or incorrect address")
        Alert.show()        
#runapp

p = Peer()
ConnectWindow()
sys.exit(app.exec())