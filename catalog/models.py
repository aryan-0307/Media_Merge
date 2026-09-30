import os
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

protected_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'protected_media'))

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MediaAsset(models.Model):
    MEDIA_TYPES = (
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio'),
    )
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='VIDEO')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='media_assets')
    language = models.CharField(max_length=50, blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)
    
    # Thumbnails can be public
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    # Media files are protected
    media_file = models.FileField(upload_to='media_files/', storage=protected_storage)
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_assets')
    publication_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DRAFT')
    is_premium = models.BooleanField(default=False, help_text="Requires active subscription to view")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class AccessKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_keys')
    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='access_keys')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"Token for {self.user.username} - {self.media_asset.title} (Valid: {self.is_valid()})"
