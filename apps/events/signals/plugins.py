# events/signals/plugins.py
from django.db.models.signals import post_save
from django.dispatch import receiver

# Drop the 'apps.' prefix from these imports
from apps.plugin_rbac.models import AdminPlugin 
from apps.events.publishers.plugins import publish_unique_plugin_purchased

@receiver(post_save, sender=AdminPlugin)
def handle_admin_plugin_purchase(sender, instance, created, **kwargs):
    print(f"--- TRACE 1: Signal caught! Created={created}, Plugin={instance.plugin.name} ---")
    
    if created:
        if getattr(instance.plugin, 'is_unique_department', False):
            publish_unique_plugin_purchased(
                admin_id=instance.admin_id,
                plugin_id=instance.plugin_id
            )