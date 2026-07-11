
from django.apps import AppConfig

class PluginRbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.plugin_rbac' # <-- Must match the path from the project root