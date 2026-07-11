# apps/user/urls.py
from django.urls import path
from .views.auth import RoleBasedLoginView

urlpatterns = [
    # This captures the role from /api/<role>/login/
    path('<str:role>/login/', RoleBasedLoginView.as_view(), name='role-based-login'),
]