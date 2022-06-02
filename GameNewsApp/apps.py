from django.apps import AppConfig


class GamenewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GameNewsApp'

    def ready(self):
        import GameNewsApp.signals