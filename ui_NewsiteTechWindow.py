from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewsiteWindow(object):
    def setupUi(self, NewsiteWindow):
        NewsiteWindow.setObjectName("NewsiteWindow")
        NewsiteWindow.resize(361, 274)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewsiteWindow.sizePolicy().hasHeightForWidth())
        NewsiteWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(NewsiteWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 30, 361, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 170, 0);")
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.backBTN = QtWidgets.QPushButton(self.centralwidget)
        self.backBTN.setGeometry(QtCore.QRect(100, 220, 75, 31))
        self.backBTN.setObjectName("backBTN")
        self.exitBTN = QtWidgets.QPushButton(self.centralwidget)
        self.exitBTN.setGeometry(QtCore.QRect(180, 220, 75, 31))
        self.exitBTN.setObjectName("exitBTN")
        self.btn_SRAN = QtWidgets.QPushButton(self.centralwidget)
        self.btn_SRAN.setGeometry(QtCore.QRect(74, 110, 75, 71))
        self.btn_SRAN.setObjectName("btn_SRAN")
        self.btn_PICO = QtWidgets.QPushButton(self.centralwidget)
        self.btn_PICO.setGeometry(QtCore.QRect(215, 110, 75, 71))
        self.btn_PICO.setObjectName("btn_PICO")
        NewsiteWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(NewsiteWindow)
        self.statusbar.setObjectName("statusbar")
        NewsiteWindow.setStatusBar(self.statusbar)

        self.retranslateUi(NewsiteWindow)
        QtCore.QMetaObject.connectSlotsByName(NewsiteWindow)

    def retranslateUi(self, NewsiteWindow):
        _translate = QtCore.QCoreApplication.translate
        NewsiteWindow.setWindowTitle(_translate("NewsiteWindow", "Newsite DWO"))
        self.label.setText(_translate("NewsiteWindow", "Please choose your newsite required technologies by clicking the corresponding checkbox"))
        self.backBTN.setText(_translate("NewsiteWindow", "Back"))
        self.exitBTN.setText(_translate("NewsiteWindow", "Exit"))
        self.btn_SRAN.setText(_translate("NewsiteWindow", "SRAN"))
        self.btn_PICO.setText(_translate("NewsiteWindow", "PICO"))

