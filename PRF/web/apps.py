from django.apps import AppConfig


class WebConfig(AppConfig):
    name = 'web'
    def ready(self):
        # everytime server restarts
        from .signals import audit_log