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
    staff_type = models.CharField(max_length=3) # e.g., 'NS', 'DR'
    
    # Nullable makes this a dual-purpose table! Nullable means for all staff in a particular role
    staff_id = models.CharField(max_length=50, null=True, blank=True) 
    
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    is_allowed = models.BooleanField()
    assigned_by = models.CharField(max_length=50)

    class Meta:
        app_label = 'plugin_rbac'
        
        indexes = [
            models.Index(fields=['admin', 'staff_type', 'staff_id']),
        ]
        
        constraints = [
            # Constraint 1: Handles specific individual user overrides (staff_id is populated)
            models.UniqueConstraint(
                fields=['admin', 'staff_type', 'staff_id', 'permission'],
                name='unique_individual_permission_override',
                condition=models.Q(staff_id__isnull=False)
            ),
            # Constraint 2: Handles global role overrides (staff_id is NULL)
            models.UniqueConstraint(
                fields=['admin', 'staff_type', 'permission'],
                name='unique_role_permission_override',
                condition=models.Q(staff_id__isnull=True)
            )
        ]