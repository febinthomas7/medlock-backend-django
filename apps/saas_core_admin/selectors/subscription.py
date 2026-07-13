from apps.plugin_rbac.models import Plugin, AdminPlugin
from apps.saas_core_admin.models.admins_hospitals import Hospital
from apps.hr_attendance_department.models.hrs import Doctor, Nurse, Receptionist
from apps.saas_core_admin.models import Subscription 

def get_admin_billing_dashboard(admin_user):
    # 1. Calculate Current Usage
    current_branches_count = Hospital.objects.filter(admin=admin_user, is_active=True).count()
    total_staff_count = (
        Doctor.objects.filter(department__hospital__admin=admin_user, is_active=True).count() +
        Nurse.objects.filter(department__hospital__admin=admin_user, is_active=True).count() +
        Receptionist.objects.filter(department__hospital__admin=admin_user, is_active=True).count()
    )

    # 2. Base mapping for UI visuals (Prices and Levels)
    # If you ever add `price` and `level` to your Django model, you can remove this dict.
    tier_mapping = {
        "Starter": {"level": 1, "price": "$0/mo"},
        "Growth": {"level": 2, "price": "$49/mo"},
        "Professional": {"level": 3, "price": "$99/mo"},
        "Enterprise": {"level": 4, "price": "$249/mo"},
        "Ultimate": {"level": 5, "price": "$499/mo"}
    }

    # 3. Get Subscription Details for current admin
    subscription_data = None
    if hasattr(admin_user, 'subscription') and admin_user.subscription:
        sub = admin_user.subscription
        subscription_data = {
            "tier_name": sub.tier_name,
            "max_branches": sub.max_branches,
            "max_staffs": sub.max_staffs,
            "current_branches": current_branches_count,
            "current_staff": total_staff_count,
            "tier_level": tier_mapping.get(sub.tier_name, {}).get("level", 1)
        }

    # 4. FETCH ALL TIERS FROM DATABASE
    all_tiers_db = Subscription.objects.all()
    available_tiers_data = []
    
    for tier in all_tiers_db:
        mapping = tier_mapping.get(tier.tier_name, {"level": 99, "price": "Custom"})
        available_tiers_data.append({
            "level": mapping["level"],
            "name": tier.tier_name,
            "maxBranches": tier.max_branches,
            "maxStaff": tier.max_staffs,
            "price": mapping["price"]
        })
        
    # Sort tiers by level so they appear correctly in the UI (1 to 5)
    available_tiers_data = sorted(available_tiers_data, key=lambda x: x["level"])

    # 5. Get Active Plugins
    active_admin_plugins = AdminPlugin.objects.filter(admin=admin_user).select_related('plugin')
    active_plugins_data = [{
        "id": str(ap.plugin.id),
        "name": ap.plugin.name,
        "prefix": ap.plugin.prefix,
        "activated_at": ap.activated_at.strftime("%Y-%m-%d")
    } for ap in active_admin_plugins]
    
    active_plugin_ids = [ap.plugin.id for ap in active_admin_plugins]

    # 6. Get Available Plugins
    available_plugins = Plugin.objects.exclude(id__in=active_plugin_ids)
    available_plugins_data = [{
        "id": str(p.id), "name": p.name, "prefix": p.prefix
    } for p in available_plugins]

    return {
        "subscription": subscription_data,
        "active_plugins": active_plugins_data,
        "available_plugins": available_plugins_data,
        "subscription_tiers": available_tiers_data  # <-- NEW DATA FOR FRONTEND
    }