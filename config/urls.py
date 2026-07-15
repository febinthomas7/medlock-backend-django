from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.user.urls')),
    path('api/', include('apps.saas_core_admin.urls')),
    path('api/rbac/', include('apps.plugin_rbac.urls')),
]