from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.utils import timezone
from decimal import Decimal

from accounts.models import User
from catalog.models import MediaAsset
from subscriptions.models import Subscription
from .models import StreamingRecord
from royalties.models import RoyaltyRecord, RoyaltyRate

def is_admin(user):
    return user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_users = User.objects.count()
    total_creators = User.objects.filter(role='CREATOR').count()
    
    total_media = MediaAsset.objects.count()
    published_media = MediaAsset.objects.filter(publication_status='PUBLISHED').count()
    
    total_subscriptions = Subscription.objects.count()
    active_subscriptions = Subscription.objects.filter(is_active=True, end_date__gt=timezone.now()).count()
    
    total_streams = StreamingRecord.objects.count()
    unprocessed_streams = StreamingRecord.objects.filter(royalty_processed=False).count()
    
    total_royalties = RoyaltyRecord.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    current_rate_obj = RoyaltyRate.objects.filter(is_active=True).first()
    current_rate = current_rate_obj.rate_per_stream if current_rate_obj else Decimal('0.0100')
    
    # Simple chart data: streams by day for the last 7 days
    from django.db.models.functions import TruncDate
    daily_streams = StreamingRecord.objects.annotate(
        date=TruncDate('started_at')
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    chart_labels = [str(ds['date']) for ds in daily_streams]
    chart_data = [ds['count'] for ds in daily_streams]
    
    context = {
        'total_users': total_users,
        'total_creators': total_creators,
        'total_media': total_media,
        'published_media': published_media,
        'total_subscriptions': total_subscriptions,
        'active_subscriptions': active_subscriptions,
        'total_streams': total_streams,
        'unprocessed_streams': unprocessed_streams,
        'total_royalties': total_royalties,
        'current_rate': current_rate,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'analytics/admin_dashboard.html', context)
