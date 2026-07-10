from django.db import models
from core.models import TimeStampedModel
from saas_core_admin.models.admins_hospitals import Admin

class Plugin(TimeStampedModel):
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name

class AdminPlugin(TimeStampedModel):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    activated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('admin', 'plugin')