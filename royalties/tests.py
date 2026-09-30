from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import MediaAsset, Category
from analytics.models import StreamingRecord
from royalties.models import RoyaltyRate, RoyaltyRecord
from royalties.services import calculate_royalties
from decimal import Decimal

User = get_user_model()

class RoyaltiesTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword')
        self.creator = User.objects.create_user(username='creator', password='password', role='CREATOR')
        self.user = User.objects.create_user(username='subscriber', password='password', role='SUBSCRIBER')
        
        self.category = Category.objects.create(name='Test Category')
        self.media = MediaAsset.objects.create(
            title='Test Media', description='Desc', category=self.category,
            creator=self.creator, publication_status='PUBLISHED'
        )
        
        # Create some streaming records
        StreamingRecord.objects.create(user=self.user, media_asset=self.media, royalty_processed=False)
        StreamingRecord.objects.create(user=self.user, media_asset=self.media, royalty_processed=False)
        
        # Create rate
        self.rate = RoyaltyRate.objects.create(rate_per_stream=Decimal('0.05'), is_active=True)

    def test_royalty_calculation(self):
        result = calculate_royalties()
        self.assertEqual(result['records_created'], 1)
        self.assertEqual(result['total_payout'], Decimal('0.10'))
        
        record = RoyaltyRecord.objects.get(media_asset=self.media)
        self.assertEqual(record.amount, Decimal('0.10'))
        
        # Check streams are marked as processed
        unprocessed = StreamingRecord.objects.filter(royalty_processed=False).count()
        self.assertEqual(unprocessed, 0)

    def test_admin_process_view(self):
        self.client.login(username='admin', password='adminpassword')
        url = reverse('royalties:process_royalties')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) # Redirects to admin dashboard
        
        # Check if processed
        record_exists = RoyaltyRecord.objects.filter(media_asset=self.media).exists()
        self.assertTrue(record_exists)
        
    def test_unauthorized_process_view(self):
        self.client.login(username='subscriber', password='password')
        url = reverse('royalties:process_royalties')
        response = self.client.post(url)
        # Assuming user_passes_test redirects to login or 403
        self.assertEqual(response.status_code, 302)
        
        # Check NOT processed
        record_exists = RoyaltyRecord.objects.filter(media_asset=self.media).exists()
        self.assertFalse(record_exists)
