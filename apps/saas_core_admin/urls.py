from django.urls import path
from .views.dashboard import AdminDashboardView

urlpatterns = [
    # ... your other endpoints like login ...
    path('ad/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]