from PySide6.QtCore import QJsonDocument
from PySide6.QtNetwork import QNetworkRequest
from typing import Dict


class JsonService:
    @staticmethod
    def dict_to_json(dict: Dict):
        doc = QJsonDocument(dict)
        return doc.toJson()

    @staticmethod
    def generate_json_request(url: str):
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        return request
