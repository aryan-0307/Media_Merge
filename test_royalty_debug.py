import os
import django
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from catalog.models import MediaAsset, Category
from analytics.models import StreamingRecord
from royalties.services import calculate_royalties
from royalties.models import RoyaltyRecord

User = get_user_model()

class DebugTest(TransactionTestCase):
    def test_debug(self):
        category = Category.objects.create(name='Movies123')
        creator = User.objects.create_user(username='c1', password='p')
        user = User.objects.create_user(username='u1', password='p')
        media = MediaAsset.objects.create(title='T1', category=category, creator=creator, is_premium=False)
        
        StreamingRecord.objects.create(user=user, media_asset=media)
        StreamingRecord.objects.create(user=user, media_asset=media)
        
        print(f"Unprocessed before calculation: {StreamingRecord.objects.filter(royalty_processed=False).count()}")
        res = calculate_royalties()
        print("calculate_royalties result:", res)
        
        print("Royalty records:", RoyaltyRecord.objects.count())
