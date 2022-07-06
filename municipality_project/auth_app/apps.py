from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'municipality_project.auth_app'

    def ready(self):
        import municipality_project.auth_app.signals

