from django.apps import AppConfig


class AllDayDJConfig(AppConfig):
    name = "alldaydj"
    verbose_name = "AllDay DJ"

    def ready(self):
        import alldaydj.signals.handlers
