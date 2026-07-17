# apps/events/publishers/plugins.py
import logging
from apps.events.dispatcher.plugins import event_dispatcher

logger = logging.getLogger(__name__)

def publish_unique_plugin_purchased(admin_id, plugin_id):
    print(f"--- TRACE 2: Publisher formatting payload for Admin {admin_id} ---")
    event_type = 'UNIQUE_PLUGIN_PURCHASED'
    payload = {'admin_id': admin_id, 'plugin_id': plugin_id}
    event_dispatcher.dispatch(event_type, payload)