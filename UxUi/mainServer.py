from PyQt6 import QtGui,QtWidgets, QtCore
import sys
import feature_server, connect_server, table, AlertWindow
sys.path.append(r".\..")
sys.path.append(r".")
from backend.mainServer import Server

ui = ''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

table_user = table.TableWindow()
table_file = table.TableWindow()
Alert = AlertWindow.Ui_Alert()

def homeUi():
    global ui
    ui = feature_server.Ui_Feature_sever()
    ui.setupUi(MainWindow)
    ui.Start_server.clicked.connect(StartClick)
    ui.Stop_server.clicked.connect(StopClick)
    ui.Showfile_btn.clicked.connect(ShowfileClick)
    ui.show_user_btn.clicked.connect(ShowuserClick)
    
    MainWindow.show()
    
def StartClick():
    try:
        server.start()   
    except:
        Alert.setupUi("The server with this address \nis already open or incorrect address")
        Alert.show()
def StopClick():
    try:
        server.shutdown() 
        app.quit()
    except:
        Alert.setupUi("The server is not started")
        Alert.show()
def ShowfileClick():
    # ui from homeUi
    filter = ui.lineEdit.text()
    data = server.get_share_files(filter) 
    result = []
    
    for (ip, port), (name, files) in data.items():
        for file in files:
            result.append([ip, port , name, file])
    table_file.setHeader(["IP","Port", "Owner", "FileName"])    
    if result != []:
        table_file.setData(result)    
        table_file.show()
    else:
        Alert.setupUi("There is no file being share")
        Alert.show()
def ShowuserClick():
    data = server.get_active_connection()
    result = []
    
    for username, (password, active) in data.items():
            result.append([username, password , active])
    table_user.setHeader(["UserName","Password", "Active"])
    if result != []:
        table_user.setData(result)    
        table_user.show()
    else:
        Alert.setupUi("There is no user online")
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
        server.setHost()
    else:
        server.setHost(ip,int(port))
    homeUi()
    
server = Server()
ConnectWindow()
sys.exit(app.exec())