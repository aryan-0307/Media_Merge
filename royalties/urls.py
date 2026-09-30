from django.urls import path
from . import views

app_name = 'royalties'

urlpatterns = [
    path('admin/process/', views.process_royalties_view, name='process_royalties'),
]
