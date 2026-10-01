import django
from django.conf import settings
import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediamerge_project.settings')
django.setup()

import json
from catalog.models import MovieDatasetRecord, MediaAsset
from django.contrib.auth import get_user_model
from subscriptions.models import Subscription
from analytics.models import StreamingRecord, WatchHistory
from royalties.models import RoyaltyRecord

User = get_user_model()

data = {
    "MovieDatasetRecord": MovieDatasetRecord.objects.count(),
    "MediaAsset": MediaAsset.objects.count(),
    "Users": User.objects.count(),
    "Subscriptions": Subscription.objects.count(),
    "StreamingRecords": StreamingRecord.objects.count(),
    "WatchHistory": WatchHistory.objects.count(),
    "RoyaltyRecords": RoyaltyRecord.objects.count()
}

print(json.dumps(data, indent=2))
