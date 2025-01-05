from models.dto.audio import Tag
from PySide6.QtCore import QAbstractListModel, Qt
from services.factory import TagService, ServiceFactory
from typing import List


class TagListModel(QAbstractListModel):
    __tags: List[Tag]
    __tag_service: TagService

    def __init__(
        self,
        *args,
        tags=None,
        tag_service: TagService = ServiceFactory().tagService(),
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__tag_service = tag_service
        self.__tags = tags or []
        self.refresh()

    def refresh(self):
        self.__tag_service.get_all_tags(self.__update_tags, None)

    def __update_tags(self, tags: List[Tag]):
        self.beginResetModel()
        self.__tags = tags
        self.endResetModel()

    def data(self, index, role):
        if role is Qt.DisplayRole:
            return self.__tags[index.row()].tag

    def rowCount(self, index):
        return len(self.__tags)
