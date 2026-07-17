from rest_framework.permissions import BasePermission
from django.core.cache import cache
from apps.plugin_rbac.selectors.permissions import get_user_allowed_permissions

class HasRBACPermission(BasePermission):
    """
    Checks if a user has access to a specific view using Redis caching.
    Requires 'required_rbac_permission' to be set on the view.
    """
    def has_permission(self, request, view):
        required_permission_name = getattr(view, 'required_rbac_permission', None)
        if not required_permission_name:
            print(f"SECURITY ALERT: View {view.__class__.__name__} is missing 'required_rbac_permission'")
            return False

        if not request.auth or not request.user:
            return False
            
        user_id = request.auth.get('user_id')
        if not user_id:
            return False

        cache_key = f"rbac_perms_user_{user_id}"
        allowed_perm_names = cache.get(cache_key)

        # Cache Miss: Calculate using the selector and store in Redis
        if allowed_perm_names is None:
            allowed_permissions_dict = get_user_allowed_permissions(request.user, request.auth)
            
            # We only need to store a flat list of permission names in Redis to keep it tiny
            allowed_perm_names = [perm.name for perm in allowed_permissions_dict.values()]
            
            cache.set(cache_key, allowed_perm_names, timeout=86400) # 24 hours

        # Final Check
        return required_permission_name in allowed_perm_names