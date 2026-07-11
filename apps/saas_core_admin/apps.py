
from django.apps import AppConfig

class SaasCoreAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.saas_core_admin' # <-- Must match the path from the project root