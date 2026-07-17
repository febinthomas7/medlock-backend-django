from django.db import models
from apps.plugin_rbac.models import PermissionMapping, PermissionOverride, AdminPlugin
from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.common.constants import ROLE_EXPANSIONS

def get_user_allowed_permissions(user, auth_payload):
    """
    Core selector to calculate a user's permissions based on their 3-tier hierarchy,
    roles, and overrides. Returns a dictionary of allowed Permission objects.
    """
    user_id = auth_payload.get('user_id')
    raw_roles = auth_payload.get('role')
    
    if not raw_roles:
        return {}
        
    if isinstance(raw_roles, str):
        raw_roles = [raw_roles]
        
    # Expand roles
    roles = []
    for r in raw_roles:
        r_lower = r.lower()
        if r_lower in ROLE_EXPANSIONS:
            roles.extend(ROLE_EXPANSIONS[r_lower])
        else:
            roles.append(r_lower)
    roles = list(dict.fromkeys(roles))
    
    if not user_id or not roles:
        return {}

    # Determine Master Admin ID
    admin_id = None
    if any(role in ['ad', 'admin'] for role in roles):
        admin_id = user_id
    elif any(role in ['hp', 'hospital'] for role in roles):
        try:
            admin_id = Hospital.objects.get(id=user_id).admin_id
        except Hospital.DoesNotExist:
            return {}
    else:
        if hasattr(user, 'department') and user.department and hasattr(user.department, 'hospital') and user.department.hospital:
            admin_id = user.department.hospital.admin_id
        if not admin_id and hasattr(user, 'hospital') and user.hospital:
            admin_id = user.hospital.admin_id
        if not admin_id and hasattr(user, 'admin_id'):
            admin_id = getattr(user, 'admin_id')

    if not admin_id:
        return {}

    # Get active plugins
    active_plugin_ids = AdminPlugin.objects.filter(
        admin_id=admin_id, is_active=True
    ).values_list('plugin_id', flat=True)

    # Fetch base permissions
    base_permissions = PermissionMapping.objects.filter(
        role__in=roles, permission__plugin_id__in=active_plugin_ids
    ).select_related('permission', 'permission__plugin')

    allowed_permissions = {mapping.permission.id: mapping.permission for mapping in base_permissions}

    # Execute Overrides
    case_insensitive_roles = [r.lower() for r in roles] + [r.upper() for r in roles]
    overrides = PermissionOverride.objects.filter(
        admin_id=admin_id,
        role_type__in=case_insensitive_roles,
        permission__plugin_id__in=active_plugin_ids
    ).filter(
        models.Q(role_id=user_id) | models.Q(role_id__isnull=True) | models.Q(role_id__exact='')
    ).select_related('permission', 'permission__plugin')

    override_list = list(overrides)
    override_list.sort(key=lambda o: 1 if o.role_id else 0)

    for override in override_list:
        perm = override.permission
        if not getattr(perm, 'is_override', True): 
            continue
            
        if override.is_allowed:
            allowed_permissions[perm.id] = perm
        else:
            if perm.id in allowed_permissions:
                del allowed_permissions[perm.id]

    return allowed_permissions