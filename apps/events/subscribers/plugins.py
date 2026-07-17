import logging
from django.utils.crypto import get_random_string

# FIX: Removed 'apps.' prefixes to match your sys.path configuration
from apps.common.constants import PLUGIN_DEPARTMENT_CONFIG
from apps.hr_attendance_department.models import Department
from apps.saas_core_admin.models import Hospital
from apps.plugin_rbac.models import Plugin

logger = logging.getLogger(__name__)

def handle_unique_plugin_rollout(payload):
    print(f"--- TRACE 3: Subscriber received payload! {payload} ---")
    admin_id = payload.get('admin_id')
    plugin_id = payload.get('plugin_id')
    
    try:
        plugin = Plugin.objects.get(id=plugin_id)
        prefix = plugin.prefix.upper()
        print(f"--- TRACE 4: Plugin prefix is '{prefix}' ---")
    except Plugin.DoesNotExist:
        print(f"--- ERROR: Plugin ID {plugin_id} not found ---")
        return

    config = PLUGIN_DEPARTMENT_CONFIG.get(prefix)
    if not config:
        print(f"--- ERROR: No rulebook config found for prefix '{prefix}' ---")
        return

    hospitals = Hospital.objects.filter(admin_id=admin_id)
    print(f"--- TRACE 5: Found {hospitals.count()} hospitals for Admin {admin_id} ---")

    for hospital in hospitals:
        print(f"--- TRACE 6: Creating department for {hospital.name} ---")
        
        try:
            # Generate a secure, random 16-character password
            random_password = get_random_string(length=16)
            
            dept, created = Department.objects.get_or_create(
                hospital=hospital,
                department_type=prefix,
                defaults={
                    'name': config['name_suffix'],
                    'password': random_password, 
                    'associated_plugin_id': plugin_id
                }
            )
            print(f"--- TRACE 7: Success! Dept '{dept.name}' Created: {created} ---")
            
        except Exception as e:
            # If the database rejects it, we will see exactly why in the terminal
            print(f"--- ❌ DATABASE ERROR for {hospital.name}: {e} ---")