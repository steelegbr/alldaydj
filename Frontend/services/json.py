from PySide6.QtCore import QJsonDocument
from typing import Dict


class JsonService:
    @staticmethod
    def dict_to_json(dict: Dict):
        doc = QJsonDocument(dict)
        return doc.toJson()
