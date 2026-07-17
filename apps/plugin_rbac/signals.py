from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import PermissionOverride, PermissionMapping

@receiver([post_save, post_delete], sender=PermissionOverride)
@receiver([post_save, post_delete], sender=PermissionMapping)
def invalidate_user_rbac_cache(sender, instance, **kwargs):
    """
    Instantly wipes the Redis cache when permissions change.
    """
    if hasattr(instance, 'role_id') and instance.role_id:
        # Wipe specific user's cache
        cache.delete(f"rbac_perms_user_{instance.role_id}")
    else:
        # If a role-wide mapping changes, wipe everything to be safe
        cache.clear()