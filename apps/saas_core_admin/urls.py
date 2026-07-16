from django.urls import path
from .views.dashboard import AdminDashboardView
from .views.hospital import AdminBranchListView
from .views.manage import HospitalManagementView, DepartmentManagementView, StaffManagementView
from .views.transfer import StaffTransferView
from .views.subscription import SubscriptionPluginDashboardView

urlpatterns = [
    # ... your other endpoints like login ...
    path('ad/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('hospital/', AdminBranchListView.as_view(), name='admin_branches'),
    path('ad/subscription/', SubscriptionPluginDashboardView.as_view(), name='admin_subscription_plugins'),
    path('manage/hospital/', HospitalManagementView.as_view(), name='admin_hospitals'),
    path('manage/department/', DepartmentManagementView.as_view(), name='admin_departments'),
    path('manage/staff/', StaffManagementView.as_view(), name='admin_staff'),
    path('staff/transfer/', StaffTransferView.as_view(), name='admin_staff_transfer'),
]
