
from django.apps import AppConfig

class PluginRbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.plugin_rbac' # <-- Must match the path from the project root

    def ready(self):
        # This line turns the signals on!
        import apps.plugin_rbac.signals