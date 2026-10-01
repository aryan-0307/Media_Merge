from django.contrib import admin
from .models import Category, MediaAsset, AccessKey, MovieDatasetRecord

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'publication_status', 'is_premium', 'created_at')
    list_filter = ('media_type', 'publication_status', 'is_premium', 'category')
    search_fields = ('title', 'description')

@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_asset', 'expires_at', 'is_valid')
    search_fields = ('user__username', 'media_asset__title')

@admin.register(MovieDatasetRecord)
class MovieDatasetRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'language', 'genre', 'rating', 'source_id')
    list_filter = ('release_year', 'language')
    search_fields = ('title', 'source_id', 'genre')
