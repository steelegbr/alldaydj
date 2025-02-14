# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clock.ui'
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
from PySide6.QtWidgets import QApplication, QLabel, QSizePolicy, QVBoxLayout, QWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(237, 178)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(7, 10, 224, 161))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.time = QLabel(self.layoutWidget)
        self.time.setObjectName("time")
        font = QFont()
        font.setPointSize(31)
        font.setBold(True)
        self.time.setFont(font)
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.time)

        self.dayOfWeek = QLabel(self.layoutWidget)
        self.dayOfWeek.setObjectName("dayOfWeek")
        font1 = QFont()
        font1.setPointSize(26)
        font1.setBold(True)
        self.dayOfWeek.setFont(font1)
        self.dayOfWeek.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.dayOfWeek)

        self.date = QLabel(self.layoutWidget)
        self.date.setObjectName("date")
        font2 = QFont()
        font2.setPointSize(20)
        font2.setBold(True)
        self.date.setFont(font2)
        self.date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.date)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.time.setText(QCoreApplication.translate("Form", "00:00:00", None))
        self.dayOfWeek.setText(QCoreApplication.translate("Form", "DayOfWeek", None))
        self.date.setText(QCoreApplication.translate("Form", "XX MonthName XXXX", None))

    # retranslateUi
