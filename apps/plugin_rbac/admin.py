from django.contrib import admin
from .models import Plugin, Permission, PermissionMapping, PermissionOverride, AdminPlugin

@admin.register(Plugin)
class PluginAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefix', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'prefix')

@admin.register(Permission)
class PermissionAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'suburl', 'plugin')
    list_filter = ('plugin',)
    search_fields = ('name', 'suburl')

admin.site.register(PermissionMapping)
admin.site.register(PermissionOverride)
admin.site.register(AdminPlugin)