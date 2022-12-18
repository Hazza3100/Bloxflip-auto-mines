import os
import sys
import random
import cloudscraper

from PyQt5           import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *


mined = []
class Mines:
    def __init__(self, token, uiData) -> None:
        self.token   = token
        self.uiData  = uiData
        self.session = cloudscraper.create_scraper() 


    def headers(self):
        return {
        'x-auth-token'      : self.token,
        }

    def createGame(self, uiData):
        try:
            nums = [0,1,2,3,4,5,6,7,8,9]
            bet_amount = uiData.betBox.text()
            if bet_amount == "Bet Amount":
                uiData.consoleText.append('Please use a valid number for amount!')

            if str(bet_amount[0:1]) in str(nums):
                
                bet = int(bet_amount)
                json = {
                    'mines'    : '3',
                    'betAmount': bet,
                }
                response = self.session.post('https://api.bloxflip.com/games/mines/create', headers=Mines(self.token, uiData).headers(), json=json)
                if response.json()['success'] == False:
                    self.uiData.consoleText.append('Error on creation')
                    return False
                if response.json()['success'] == True:
                    uiData.consoleText.append(f"[+] Game created with id: {response.json()['game']['uuid']}")
                    return True
                else:
                    return False
            else:
                None
        except:
            pass

    def cashout(self, uiData):
        try:
            with self.session as session:
                json = {
                    'cashout': True,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token, uiData).headers(), json=json)
                if response.json()['success'] == True:
                    self.uiData.consoleText.append(f"You won: {round(response.json()['winnings'])}")
                # if "You do not have an active mines game!" in response.text:
                #     self.uiData.consoleText.append(f"Error - You don't have a active game")
                # else:
                #     self.uiData.consoleText.append('Unkown Error - 404')
        except:
            pass
    
    def fmine(self, uiData):
        try:
            with self.session as session:
                coord = random.randint(1,24)
                if coord in mined:
                    coord = random.randint(1,24)
                else:
                    mined.append(coord)
                json = {
                    'cashout': False,
                    'mine': coord,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token, uiData).headers(), json=json)
                if response.json()['success'] == True:
                    uiData.consoleText.append('Mine 1 - success')
                    uiData.consoleText.append(f"Multipler: {round(response.json()['multiplier'], 2)}")
                    return True
                else:
                    return False
        except:
            pass

    def smine(self, uiData):
        try:
            with self.session as session:
                coord = random.randint(1,24)
                if coord in mined:
                    coord = random.randint(1,24)
                else:
                    mined.append(coord)
                json = {
                    'cashout': False,
                    'mine'   : coord,
                }
                response = session.post('https://api.bloxflip.com/games/mines/action', headers=Mines(self.token, uiData).headers(), json=json)
                if response.json()['success'] == True:
                    uiData.consoleText.append(f"Multipler: {round(response.json()['multiplier'], 2)}")
                    return True
                else:
                    return False
        except:
            pass


    def handle(self, uiData):
        uuid  = self.createGame(uiData)
        if uuid == False:
            None
        if uuid == True:
            mine = self.fmine(uiData)

            if mine == True:
                mine2 = self.smine(uiData)
                if mine2 == True:
                    uiData.consoleText.append('Mine 2 - success')
                    x = uiData.againCheckBox.isChecked()
                    if x == True:
                        mine3 = self.smine(uiData)
                        if mine3 == True:
                            self.cashout(uiData)
                            uiData.consoleText.append('Mine 3 - success, cashed out')
                        else:
                            uiData.consoleText.append('Mined a bomb should of cashed out smh')
                    if x == False:
                        self.cashout(uiData)
                    # else:
                    #     self.cashout(uiData)
                    self.cashout(uiData)
                else:
                    self.cashout(uiData)
            else:
                uiData.consoleText.append('Mine 1 - Error')





class MinesUi(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(536, 393)
        MainWindow.setMinimumSize(QSize(300, 320))
        MainWindow.setMaximumSize(QSize(536, 393))
        MainWindow.setStyleSheet(u"background-color: #151720;")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionhello = QAction(MainWindow)
        self.actionhello.setObjectName(u"actionhello")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.TitleLabel = QLabel(self.centralwidget)
        self.TitleLabel.setObjectName(u"TitleLabel")
        self.TitleLabel.setGeometry(QRect(205, -2, 131, 41))
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
        self.consoleLabel.setGeometry(QRect(70, 180, 401, 31))
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
        self.consoleText.setGeometry(QRect(70, 210, 401, 171))
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
        self.StartButton.setGeometry(QRect(15, 90, 81, 31))
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
        self.cashoutButton.setGeometry(QRect(445, 90, 81, 31))
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
        self.tokenBox.setGeometry(QRect(20, 40, 501, 31))
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
        self.ExitButton = QPushButton(self.centralwidget)
        self.ExitButton.setObjectName(u"ExitButton")
        self.ExitButton.setEnabled(True)
        self.ExitButton.setGeometry(QRect(15, 130, 81, 31))
        self.ExitButton.setFont(font2)
        self.ExitButton.setStyleSheet(u"QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #c72626;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    color: rgb(255, 255, 255);\n"
"    border-top-left-radius: 10;\n"
"    border-bottom-left-radius: 10;\n"
"    border-bottom-right-radius: 10;\n"
"    border-top-right-radius: 10;\n"
"    background-color: #a32626;\n"
"}")
        self.betBox = QLineEdit(self.centralwidget)
        self.betBox.setObjectName(u"betBox")
        self.betBox.setGeometry(QRect(225, 90, 91, 31))
        self.betBox.setFont(font3)
        self.betBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-top-left-radius: 10;\n"
"border-bottom-left-radius: 10;\n"
"border-bottom-right-radius: 10;\n"
"border-top-right-radius: 10;\n"
"border: 1px solid #817ad7;")
        self.betBox.setAlignment(Qt.AlignCenter)
        self.continueButton = QPushButton(self.centralwidget)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setEnabled(True)
        self.continueButton.setGeometry(QRect(445, 130, 81, 31))
        self.continueButton.setFont(font2)
        self.continueButton.setStyleSheet(u"QPushButton {\n"
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
        self.againCheckBox = QCheckBox(self.centralwidget)
        self.againCheckBox.setObjectName(u"againCheckBox")
        self.againCheckBox.setGeometry(QRect(225, 130, 91, 31))
        font4 = QFont()
        font4.setPointSize(12)
        self.againCheckBox.setFont(font4)
        self.againCheckBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-top-left-radius: 10;\n"
"border-bottom-left-radius: 10;\n"
"border-bottom-right-radius: 10;\n"
"border-top-right-radius: 10;\n"
"border: 1px solid #817ad7;")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        self.StartButton.clicked.connect(self.start)
        self.ExitButton.clicked.connect(self.exit)
        self.cashoutButton.clicked.connect(self.cash)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Auto Mines -  Sandwich", None))
        self.actionhello.setText(QCoreApplication.translate("MainWindow", u"hello!", None))
        self.TitleLabel.setText(QCoreApplication.translate("MainWindow", u"Auto mines", None))
        self.consoleLabel.setText(QCoreApplication.translate("MainWindow", u"Console", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.cashoutButton.setText(QCoreApplication.translate("MainWindow", u"Cashout", None))
        self.tokenBox.setText(QCoreApplication.translate("MainWindow", u"Token", None))
        self.ExitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.betBox.setText(QCoreApplication.translate("MainWindow", u"Bet Amount", None))
        self.continueButton.setText(QCoreApplication.translate("MainWindow", u"Continue", None))
        self.againCheckBox.setText(QCoreApplication.translate("MainWindow", u"3x?", None))


    def start(self):
        token = self.tokenBox.text()
        Mines(token, self).handle(self)

    def exit(self):
        os._exit(0)

    def cash(self):
        token = self.tokenBox.text()
        Mines(token, self).cashout(self)


def gui():
    app = QtWidgets.QApplication(sys.argv)
    ex = MinesUi()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())




gui()
