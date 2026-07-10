from django.contrib import admin
from .models import (
    Department, Doctor, Nurse, Receptionist, 
    Ward, Room, Bed, StaffAttendance, BiometricPunch
)

@admin.register(Doctor)
class DoctorAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'designation', 'is_active')
    search_fields = ('name', 'id')
    list_filter = ('department', 'is_active')

@admin.register(StaffAttendance)
class AttendanceAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'staff_id', 'staff_role', 'date', 'status')
    list_filter = ('status', 'date', 'staff_role')
    search_fields = ('staff_id',)

@admin.register(Bed)
class BedAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'bed_identifier', 'room', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('bed_identifier',)

admin.site.register(Department)
admin.site.register(Nurse)
admin.site.register(Receptionist)
admin.site.register(Ward)
admin.site.register(Room)
admin.site.register(BiometricPunch)