from django.db import models
from core.models import TimeStampedModel
from apps.saas_core_admin.models.admins_hospitals import Admin
from .plugins import Plugin

class Permission(TimeStampedModel):
    class Meta:
        app_label = 'plugin_rbac'

    name = models.CharField(max_length=100)
    suburl = models.CharField(max_length=100)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PermissionMapping(TimeStampedModel):

    role = models.CharField(max_length=3)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    requires_on_premise = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('role', 'permission'),
        app_label = 'plugin_rbac'

class PermissionOverride(TimeStampedModel):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=3)
    staff_id = models.CharField(max_length=50) 
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    is_allowed = models.BooleanField()
    assigned_by = models.CharField(max_length=50)

    class Meta:
        unique_together = ('staff_id', 'staff_type', 'permission'),
        app_label = 'plugin_rbac'
        indexes = [
            # This creates a combined index for the most common lookup pattern
            models.Index(fields=['staff_id', 'staff_type']),
        ]