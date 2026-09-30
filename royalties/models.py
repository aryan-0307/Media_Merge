from django.db import models
from django.conf import settings
from catalog.models import MediaAsset

class RoyaltyRate(models.Model):
    rate_per_stream = models.DecimalField(max_digits=10, decimal_places=4, default=0.0100)
    effective_from = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active rate exists
            RoyaltyRate.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"${self.rate_per_stream} per stream (Active: {self.is_active})"

class RoyaltyRecord(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='royalty_records')
    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='royalty_records')
    streams_counted = models.PositiveIntegerField()
    rate_applied = models.DecimalField(max_digits=10, decimal_places=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator.username} - {self.media_asset.title}: ${self.amount}"
