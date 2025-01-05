from datetime import datetime, timezone
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow
from ui.views.generated.clock import Ui_Form as BaseClock


class Clock(QMainWindow, BaseClock):
    __timer: QTimer

    def __init__(self, refresh_interval: int = 500):
        super().__init__()
        self.setupUi(self)

        self.__timer = QTimer(self)

        self.__timer.timeout.connect(self.__update_time)
        self.__timer.start(refresh_interval)

        self.__update_time()

        self.setMinimumHeight(178)

    def __update_time(self):
        now = datetime.now(timezone.utc).astimezone()

        self.time.setText(now.strftime("%H:%M:%S"))
        self.dayOfWeek.setText(now.strftime("%A"))
        self.date.setText(now.strftime("%d %B %Y"))
