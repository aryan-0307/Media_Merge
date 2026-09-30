from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
