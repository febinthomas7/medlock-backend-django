from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models  # Required for models.Q
from apps.plugin_rbac.models import Permission, PermissionMapping, PermissionOverride, AdminPlugin
from apps.saas_core_admin.models.admins_hospitals import Admin, Hospital

class DynamicNavigationView(APIView):
    # Assuming you have JWT authentication set up
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Extract user data from your custom JWT payload
        user_id = request.auth.get('user_id')
        raw_roles = request.auth.get('role')
        
        # Ensure raw_roles is a list (handles both string and array formats)
        if not raw_roles:
            return Response({"navigation": []}, status=200)
            
        if isinstance(raw_roles, str):
            raw_roles = [raw_roles]
            
        # Complete mapping for both abbreviations and full-length role names
        ROLE_EXPANSIONS = {
            'admin': ['admin', 'ad'],
            'ad': ['admin', 'ad'],
            'hospital': ['hospital', 'hp'],
            'hp': ['hospital', 'hp'],
            'department': ['department', 'dp'],
            'dp': ['department', 'dp'],
            'doctor': ['doctor', 'dr'],
            'dr': ['doctor', 'dr'],
            'nurse': ['nurse', 'ns'],
            'ns': ['nurse', 'ns'],
            'receptionist': ['receptionist', 'rs'],
            'rs': ['receptionist', 'rs'],
        }

        # Expand roles so that 'dr' -> ['dr', 'doctor'], 'admin' -> ['admin', 'ad'], etc.
        roles = []
        for r in raw_roles:
            r_lower = r.lower()
            if r_lower in ROLE_EXPANSIONS:
                roles.extend(ROLE_EXPANSIONS[r_lower])
            else:
                roles.append(r_lower)
        
        # Remove any duplicates while keeping order
        roles = list(dict.fromkeys(roles))
        
        if not user_id or not roles:
            return Response({"navigation": []}, status=200)

        # 2. Determine the Master Admin ID (Tenant ID) based on the hierarchy chain
        admin_id = None
        
        if any(role in ['ad', 'admin'] for role in roles):
            # Tier 1: User is the Admin (Tenant root)
            admin_id = user_id
            
        elif any(role in ['hp', 'hospital'] for role in roles):
            # Tier 2: User is a Hospital (Get admin_id directly from the Hospital entry)
            try:
                hospital = Hospital.objects.get(id=user_id)
                admin_id = hospital.admin_id
            except Hospital.DoesNotExist:
                return Response({"navigation": []}, status=200)
                
        else:
            # Tier 3 & 4: Staff/Department (dr, ns, rs, dp) linked via Department -> Hospital -> Admin
            if hasattr(request.user, 'department') and request.user.department:
                dept = request.user.department
                if hasattr(dept, 'hospital') and dept.hospital:
                    admin_id = dept.hospital.admin_id
            
            # Fallback 1: Direct link to hospital (if department is bypassed)
            if not admin_id and hasattr(request.user, 'hospital') and request.user.hospital:
                admin_id = request.user.hospital.admin_id

            # Fallback 2: System attach legacy property
            if not admin_id and hasattr(request.user, 'admin_id'):
                admin_id = getattr(request.user, 'admin_id')

        # Safety catch: If we still don't know the Admin ID, block access
        if not admin_id:
            print(f"SECURITY BLOCK: Could not resolve admin_id for user {user_id} with roles {roles}")
            return Response({"navigation": []}, status=200)

        # 3. Get ONLY the active plugins for this Admin's Network
        active_plugin_ids = AdminPlugin.objects.filter(
            admin_id=admin_id,
            is_active=True
        ).values_list('plugin_id', flat=True)

        # 4. Fetch all permissions mapped to ALL resolved roles for active plugins
        # select_related('permission__plugin') is required so we can group by plugin name later
        base_permissions = PermissionMapping.objects.filter(
            role__in=roles,
            permission__plugin_id__in=active_plugin_ids
        ).select_related('permission', 'permission__plugin')

        # Dictionary prevents duplicate permissions when a user matches multiple roles
        allowed_permissions = {}

        # 5. Execute your 3-Tier Security Hierarchy Check
        for mapping in base_permissions:
            perm = mapping.permission
            
            # Skip if already authorized from a previous role in the array evaluation
            if perm.id in allowed_permissions:
                continue
            
            if not getattr(perm, 'allow_override', False): # Safely check in case field isn't there yet
                allowed_permissions[perm.id] = perm
                continue
                
            # Check for explicit block/allow overrides (Role-wide OR Individual)
            override = PermissionOverride.objects.filter(
                admin_id=admin_id,
                staff_type__in=roles,
                permission=perm
            ).filter(
                models.Q(staff_id=user_id) | models.Q(staff_id__isnull=True)
            ).order_by('-staff_id').first() # staff_id sorts before NULL, putting individual rules first

            if override:
                if override.is_allowed:
                    allowed_permissions[perm.id] = perm
            else:
                # No override exists, rely on base mapping
                allowed_permissions[perm.id] = perm

        # 6. Group by Plugin (Tab) and Permission (Sub-tab)
        nav_dict = {}
        
        for perm in allowed_permissions.values():
            plugin_name = perm.plugin.name 
            
            # Create the Plugin tab if it doesn't exist yet
            if plugin_name not in nav_dict:
                nav_dict[plugin_name] = {
                    "name": plugin_name,
                    "subItems": []
                }
            
            # Use tab_name for the sub-tab, but safely fallback to perm.name if it's empty
            sub_tab_name = perm.tab_name if perm.tab_name and perm.tab_name.strip().lower() != 'none' else perm.name

            # Append the Permission as a sub-tab inside the Plugin
            nav_dict[plugin_name]["subItems"].append({
                "name": sub_tab_name,
                "href": perm.suburl
            })

        # Convert dictionary to array
        final_navigation = list(nav_dict.values())

        return Response({"navigation": final_navigation}, status=200)