from django.db import models
from django.conf import settings
from catalog.models import MediaAsset

class StreamingRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streaming_records')
    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='streaming_records')
    started_at = models.DateTimeField(auto_now_add=True)
    royalty_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} watched {self.media_asset.title} at {self.started_at}"

class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_history')
    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='watch_history')
    progress_seconds = models.PositiveIntegerField(default=0)
    last_watched = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'media_asset')

    def __str__(self):
        return f"{self.user.username} history for {self.media_asset.title}"
