# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher.ui'
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
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 351)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 787, 332))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.banner = QLabel(self.layoutWidget)
        self.banner.setObjectName("banner")
        self.banner.setPixmap(QPixmap("ui/assets/banner.jpg"))

        self.verticalLayout.addWidget(self.banner)

        self.instanceUrlLabel = QLabel(self.layoutWidget)
        self.instanceUrlLabel.setObjectName("instanceUrlLabel")

        self.verticalLayout.addWidget(self.instanceUrlLabel)

        self.instanceUrl = QLineEdit(self.layoutWidget)
        self.instanceUrl.setObjectName("instanceUrl")

        self.verticalLayout.addWidget(self.instanceUrl)

        self.login = QPushButton(self.layoutWidget)
        self.login.setObjectName("login")

        self.verticalLayout.addWidget(self.login)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "AllDay DJ", None)
        )
        self.banner.setText("")
        self.instanceUrlLabel.setText(
            QCoreApplication.translate("MainWindow", "Instance URL:", None)
        )
        self.login.setText(QCoreApplication.translate("MainWindow", "Log In", None))

    # retranslateUi
