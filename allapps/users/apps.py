from importlib import import_module

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "allapps.users"

    def ready(self):
        import_module("allapps.users.signals")
