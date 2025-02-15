# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy, QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(559, 203)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.throbber = QLabel(self.centralwidget)
        self.throbber.setObjectName("throbber")
        self.throbber.setGeometry(QRect(20, 20, 171, 151))
        self.code = QLabel(self.centralwidget)
        self.code.setObjectName("code")
        self.code.setGeometry(QRect(230, 110, 311, 51))
        font = QFont()
        font.setPointSize(45)
        font.setBold(True)
        self.code.setFont(font)
        self.code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status = QLabel(self.centralwidget)
        self.status.setObjectName("status")
        self.status.setGeometry(QRect(230, 40, 311, 51))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Logging In...", None)
        )
        self.throbber.setText("")
        self.code.setText(QCoreApplication.translate("MainWindow", "ABCD-1234", None))
        self.status.setText(
            QCoreApplication.translate("MainWindow", "Some status goes here...", None)
        )

    # retranslateUi
