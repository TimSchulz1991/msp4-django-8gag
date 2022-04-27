from django.apps import AppConfig


class My8GagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my8gag'

    def ready(self):
        import my8gag.signals
