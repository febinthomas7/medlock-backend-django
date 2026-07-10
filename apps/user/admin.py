from django.contrib import admin
from .models import (
    User, EmergencyContact, UserAppointment, UserBloodAppointment, 
    UserBloodDonation, UserEvent, UserReport
)

@admin.register(User)
class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'gmail', 'contact', 'is_active', 'created_at')
    search_fields = ('name', 'gmail', 'contact', 'id')
    list_filter = ('is_active', 'created_at')

@admin.register(EmergencyContact)
class EmergencyContactAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'relation', 'contact_number', 'is_primary')
    list_filter = ('is_primary', 'relation')
    search_fields = ('name', 'user__name', 'contact_number')

@admin.register(UserAppointment)
class AppointmentAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'scheduled_at', 'status')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('user__name', 'doctor__name', 'id')

@admin.register(UserBloodDonation)
class BloodDonationAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'user', 'blood_group', 'donation_date', 'component_type')
    list_filter = ('blood_group', 'component_type', 'donation_date')
    search_fields = ('user__name', 'id')

admin.site.register(UserBloodAppointment)
admin.site.register(UserEvent)
admin.site.register(UserReport)