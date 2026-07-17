# events/apps.py
from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Must match the exact string in INSTALLED_APPS
    name = 'events' 

    def ready(self):
        print(">>> 🚀 EVENT BUS IGNITION: ready() method is firing! <<<") 
        try:
            # Drop the 'apps.' prefix here as well
            import events.signals.plugins
            print(">>> 🔌 SIGNALS IMPORTED SUCCESSFULLY <<<")
        except Exception as e:
            print(f">>> ❌ SIGNAL IMPORT FAILED: {e} <<<")