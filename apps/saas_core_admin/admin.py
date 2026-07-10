from django.contrib import admin
from .models import Admin, Hospital, Subscription, Theme

@admin.register(Admin)
class SaaSAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'id')
    list_filter = ('is_active', 'subscription')

@admin.register(Hospital)
class HospitalAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin', 'is_active')
    search_fields = ('name', 'id')
    list_filter = ('is_active',)

admin.site.register(Subscription)
admin.site.register(Theme)