from django.db import transaction
from django.db.models import Count
from analytics.models import StreamingRecord
from .models import RoyaltyRate, RoyaltyRecord
from catalog.models import MediaAsset
from decimal import Decimal

def calculate_royalties():
    """
    Calculates royalties for all eligible, unprocessed streaming records.
    Returns the total amount processed.
    """
    with transaction.atomic():
        # Get active rate
        rate_obj = RoyaltyRate.objects.filter(is_active=True).first()
        if not rate_obj:
            # If no rate exists, create a default one
            rate_obj = RoyaltyRate.objects.create()
            
        rate = rate_obj.rate_per_stream
        
        # Get unprocessed streams grouped by media asset
        unprocessed_streams = StreamingRecord.objects.filter(
            royalty_processed=False
        ).values('media_asset_id').annotate(
            stream_count=Count('id')
        )
        
        total_payout = Decimal('0.00')
        records_created = 0
        
        for item in unprocessed_streams:
            media_id = item['media_asset_id']
            stream_count = item['stream_count']
            
            # Fetch media
            media = MediaAsset.objects.select_related('creator').get(pk=media_id)
            
            # Calculate amount using Decimal
            amount = Decimal(stream_count) * rate
            
            # Create royalty record
            RoyaltyRecord.objects.create(
                creator=media.creator,
                media_asset=media,
                streams_counted=stream_count,
                rate_applied=rate,
                amount=amount
            )
            
            # Mark streams as processed
            # Use a bulk update for efficiency
            StreamingRecord.objects.filter(
                media_asset_id=media_id, 
                royalty_processed=False
            ).update(royalty_processed=True)
            
            total_payout += amount
            records_created += 1
            
        return {
            'records_created': records_created,
            'total_payout': total_payout,
            'rate_applied': rate
        }
