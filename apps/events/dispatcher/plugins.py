# apps/events/dispatcher/plugins.py

from events.subscribers.plugins import handle_unique_plugin_rollout
import logging

logger = logging.getLogger(__name__)

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def register(self, event_type, listener_func):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener_func)
        logger.info(f"Registered listener for {event_type}")

    def dispatch(self, event_type, payload):
        listeners = self.listeners.get(event_type, [])
        for listener in listeners:
            try:
                listener(payload)
            except Exception as e:
                logger.error(f"Error executing listener for {event_type}: {str(e)}")

# Instantiate the singleton
event_dispatcher = EventDispatcher()


event_dispatcher.register('UNIQUE_PLUGIN_PURCHASED', handle_unique_plugin_rollout)