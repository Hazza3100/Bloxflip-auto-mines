import os
import random
import sys
import cloudscraper

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 


mined = []
bet   = 5
class Mines:
    def __init__(self, token, uiData) -> None:
        self.token   = token
        self.uiData  = uiData
        self.session = cloudscraper.create_scraper() 


    def headers(self):
        return {
        'x-auth-token'      : self.token,
        }


    def createGame(self):
        try:
            json = {
                'mines'    : '3',
                'betAmount': bet,
            }
            response = self.session.post('https://api.bloxflip.com/games/mines/create', headers=Mines(self.token).headers(), json=json)
            if response.json()['success'] == False:
                self.uiData.consoleText.append('Mined a bomb should of cashed out smh')
                return False
            else:
                return response.json()['game']['uuid']
        except:
            pass

    def cashout(self):
        try:
            with self.session as session:
                json = {
                    'cashout': True,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token).headers(), json=json)
                if response.json()['success'] == True:
                    self.uiData.consoleText.append(f"You won: {round(response.json()['winnings'])}")
                else:
                    self.uiData.consoleText.append(f"Error")
        except:
            pass
    
    def fmine(self):
        try:
            with self.session as session:
                coord = random.randint(1,25)
                if coord in mined:
                    coord = random.randint(1,25)
                else:
                    mined.append(coord)
                json = {
                    'cashout': False,
                    'mine': coord,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token).headers(), json=json)
                print(response.text)
                if response.json()['success'] == True:
                    print("First mine good")
                    print(f"Multipler: {round(response.json()['multiplier'], 2)}")
                    return True
                else:
                    return False
        except Exception as e:
            print(e)

    def smine(self):
        try:
            with self.session as session:
                coord = random.randint(1,25)
                if coord in mined:
                    coord = random.randint(1,25)
                else:
                    mined.append(coord)
                json = {
                    'cashout': False,
                    'mine'   : 13,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token).headers(), json=json)
                if response.json()['success'] == True:
                    print("Second mine good")
                    self.uiData.consoleText.append('Mined a bomb should of cashed out smh')
                    return True
                else:
                    return False
        except:
            pass


    def handle(self, uiData):
        uuid  = self.createGame(uiData)
        if uuid == False:
            pass
        else:
            mine  = self.fmine()

            if mine == True:
                mine2 = self.smine()
                if mine2 == True:
                    uiData.consoleText.append('Mined 2 mines! Success')
                    self.cashout()
                    # x = uiData.againBox.text()
                    # if x == "y/n":
                    #     mine3 = self.smine()
                    #     if mine3 == True:
                    #         self.cashout()
                    #     else:
                    #         uiData.consoleText.append('Mined a bomb should of cashed out smh')
                    #         # print("Mined a bomb should of cashed out smh")
                else:
                    self.cashout()
            else:
                uiData.consoleText.append('First mine error')





class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 320)
        MainWindow.setMinimumSize(QSize(300, 320))
        MainWindow.setMaximumSize(QSize(300, 320))
        MainWindow.setStyleSheet(u"background-color: #151720;")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionhello = QAction(MainWindow)
        self.actionhello.setObjectName(u"actionhello")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.TitleLabel = QLabel(self.centralwidget)
        self.TitleLabel.setObjectName(u"TitleLabel")
        self.TitleLabel.setGeometry(QRect(80, 0, 131, 41))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setStyleSheet(u"color: #867edf;\n"
"background-color: rgba(255, 0, 0, 0);")
        self.TitleLabel.setAlignment(Qt.AlignCenter)
        self.consoleLabel = QLabel(self.centralwidget)
        self.consoleLabel.setObjectName(u"consoleLabel")
        self.consoleLabel.setGeometry(QRect(20, 140, 261, 31))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        self.consoleLabel.setFont(font1)
        self.consoleLabel.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-top-left-radius: 15;\n"
"border-bottom-left-radius: 0;\n"
"border-bottom-right-radius: 0;\n"
"border-top-right-radius: 15;\n"
"border: 2px solid #817ad7;")
        self.consoleLabel.setAlignment(Qt.AlignCenter)
        self.consoleText = QTextEdit(self.centralwidget)
        self.consoleText.setObjectName(u"consoleText")
        self.consoleText.setGeometry(QRect(20, 170, 261, 131))
        self.consoleText.setLayoutDirection(Qt.LeftToRight)
        self.consoleText.setStyleSheet(u"background-color: rgb(43, 41, 41);\n"
"color: rgb(255, 255, 255);\n"
"\n"
"\n"
"border-bottom-left-radius: 15;\n"
"border-bottom-right-radius: 15;\n"
"border: 2px solid #817ad7;")
        self.StartButton = QPushButton(self.centralwidget)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setEnabled(True)
        self.StartButton.setGeometry(QRect(50, 100, 81, 31))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setWeight(75)
        self.StartButton.setFont(font2)
        self.StartButton.setStyleSheet(u"QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #5549d1;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #4637de;\n"
"}")
        self.cashoutButton = QPushButton(self.centralwidget)
        self.cashoutButton.setObjectName(u"cashoutButton")
        self.cashoutButton.setEnabled(True)
        self.cashoutButton.setGeometry(QRect(170, 100, 81, 31))
        self.cashoutButton.setFont(font2)
        self.cashoutButton.setStyleSheet(u"QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #5549d1;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #4637de;\n"
"}")
        self.tokenBox = QLineEdit(self.centralwidget)
        self.tokenBox.setObjectName(u"tokenBox")
        self.tokenBox.setGeometry(QRect(110, 50, 81, 31))
        font3 = QFont()
        font3.setPointSize(11)
        self.tokenBox.setFont(font3)
        self.tokenBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-top-left-radius: 10;\n"
"border-bottom-left-radius: 10;\n"
"border-bottom-right-radius: 10;\n"
"border-top-right-radius: 10;\n"
"border: 1px solid #817ad7;")
        self.tokenBox.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        self.StartButton.clicked.connect(self.start)
        self.cashoutButton.clicked.connect(self.cash)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Auto Mines -  Sandwich", None))
        self.actionhello.setText(QCoreApplication.translate("MainWindow", u"hello!", None))
        self.TitleLabel.setText(QCoreApplication.translate("MainWindow", u"Auto mines", None))
        self.consoleLabel.setText(QCoreApplication.translate("MainWindow", u"Console", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.cashoutButton.setText(QCoreApplication.translate("MainWindow", u"Cashout", None))
        self.tokenBox.setText(QCoreApplication.translate("MainWindow", u"Token", None))
    
    def start(self):
        token = self.tokenBox.text()
        Mines(token, self).handle(self)

    def cash(self):
        token = self.tokenBox.text()
        Mines(token, self).cashout()


def gui():
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())




gui()
