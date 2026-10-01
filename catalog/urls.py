from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('browse/', views.browse_view, name='browse'),
    path('media/<int:pk>/', views.media_detail_view, name='media_detail'),
    path('media/<int:pk>/token/', views.generate_access_token, name='generate_token'),
    path('media/<int:pk>/progress/', views.update_progress, name='update_progress'),
    path('stream/<uuid:token>/', views.stream_media, name='stream_media'),
    
    # Creator tools
    path('creator/dashboard/', views.creator_dashboard_view, name='creator_dashboard'),
    path('creator/upload/', views.media_upload_view, name='media_upload'),
    path('creator/<int:pk>/edit/', views.media_edit_view, name='media_edit'),
    path('creator/<int:pk>/delete/', views.media_delete_view, name='media_delete'),
    
    # Movie Database
    path('movie-database/', views.movie_database_list_view, name='movie_database_list'),
    path('movie-database/<int:pk>/', views.movie_database_detail_view, name='movie_database_detail'),
]

