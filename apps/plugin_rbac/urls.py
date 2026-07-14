from django.urls import path
from .views.navigation import DynamicNavigationView

urlpatterns = [
    path('navigation/', DynamicNavigationView.as_view(), name='dynamic-nav'),
]