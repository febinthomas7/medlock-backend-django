
from django.apps import AppConfig

class HrAttendanceDepartmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hr_attendance_department' # <-- Must match the path from the project root