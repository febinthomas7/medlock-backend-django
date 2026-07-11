from django.db import models
from core.models import TimeStampedModel
from apps.saas_core_admin.models.admins_hospitals import Admin

class Plugin(TimeStampedModel):
    class Meta:
        app_label = 'plugin_rbac'

    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name

class AdminPlugin(TimeStampedModel):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    activated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('admin', 'plugin'),
        app_label = 'plugin_rbac'