# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(742, 332)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 787, 332))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.banner = QLabel(self.widget)
        self.banner.setObjectName(u"banner")
        self.banner.setPixmap(QPixmap(u"./ui/assets/banner.jpg"))

        self.verticalLayout.addWidget(self.banner)

        self.instanceUrlLabel = QLabel(self.widget)
        self.instanceUrlLabel.setObjectName(u"instanceUrlLabel")

        self.verticalLayout.addWidget(self.instanceUrlLabel)

        self.instanceUrl = QLineEdit(self.widget)
        self.instanceUrl.setObjectName(u"instanceUrl")

        self.verticalLayout.addWidget(self.instanceUrl)

        self.login = QPushButton(self.widget)
        self.login.setObjectName(u"login")

        self.verticalLayout.addWidget(self.login)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AllDay DJ", None))
        self.banner.setText("")
        self.instanceUrlLabel.setText(QCoreApplication.translate("MainWindow", u"Instance URL:", None))
        self.login.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
    # retranslateUi

