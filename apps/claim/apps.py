
from django.apps import AppConfig

class ClaimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.claim' # <-- Must match the path from the project root