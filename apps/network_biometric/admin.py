from django.contrib import admin
from .models import HospitalNetwork, AdminNetwork, BiometricDeviceMapping

@admin.register(BiometricDeviceMapping)
class DeviceMappingAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'device_ip', 'punch_id', 'staff_role', 'is_currently_assigned')
    list_filter = ('is_currently_assigned', 'staff_role')
    search_fields = ('device_ip', 'punch_id')

admin.site.register(HospitalNetwork)
admin.site.register(AdminNetwork)