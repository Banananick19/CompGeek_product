from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready():
        import CompGeek.main.signals.handlers