from django.db import transaction
from apps.plugin_rbac.models import Plugin, AdminPlugin

def activate_plugin_for_admin(admin_user, plugin_id):
    """Activates a plugin for an admin if they don't already have it."""
    if not plugin_id:
        raise ValueError("Plugin ID is required.")

    plugin = Plugin.objects.get(id=plugin_id)
    
    # Check if already activated
    if AdminPlugin.objects.filter(admin=admin_user, plugin=plugin).exists():
        raise ValueError(f"You have already activated the {plugin.name} plugin.")

    with transaction.atomic():
        admin_plugin = AdminPlugin.objects.create(
            admin=admin_user,
            plugin=plugin
        )
        
    return {
        "id": str(plugin.id),
        "name": plugin.name,
        "prefix": plugin.prefix,
        "activated_at": admin_plugin.activated_at.strftime("%Y-%m-%d %H:%M:%S")
    }