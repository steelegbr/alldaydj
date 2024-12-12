from PySide6.QtCore import QByteArray
from PySide6.QtNetwork import QNetworkReply
from typing import List, Optional


class MockSignal:
    connect_callbacks: List[callable]

    def __init__(self):
        self.connect_callbacks = []

    def connect(self, callback: callable):
        self.connect_callbacks.append(callback)


class MockQtHttpResponse:
    __error: Optional[QNetworkReply.NetworkError]
    __response: QByteArray

    def __init__(self, response: str, error: QNetworkReply.NetworkError = None):
        self.__error = error
        self.__response = QByteArray(response.encode())

    def readAll(self):
        return self.__response

    def error(self):
        return self.__error
