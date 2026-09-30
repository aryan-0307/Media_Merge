from django.contrib import admin
from .models import RoyaltyRate, RoyaltyRecord

@admin.register(RoyaltyRate)
class RoyaltyRateAdmin(admin.ModelAdmin):
    list_display = ('rate_per_stream', 'is_active', 'effective_from')
    list_filter = ('is_active',)

@admin.register(RoyaltyRecord)
class RoyaltyRecordAdmin(admin.ModelAdmin):
    list_display = ('creator', 'media_asset', 'streams_counted', 'amount', 'calculated_at')
    list_filter = ('calculated_at', 'creator')
    search_fields = ('creator__username', 'media_asset__title')
    readonly_fields = ('creator', 'media_asset', 'streams_counted', 'rate_applied', 'amount', 'calculated_at')
