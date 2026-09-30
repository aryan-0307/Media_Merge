from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid
import os
from django.conf import settings

from catalog.models import MediaAsset, Category, AccessKey
from subscriptions.models import Subscription, SubscriptionPlan
from analytics.models import StreamingRecord, WatchHistory

User = get_user_model()

class CatalogTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.creator = User.objects.create_user(username='creator', password='password', role='CREATOR')
        self.subscriber = User.objects.create_user(username='subscriber', password='password', role='SUBSCRIBER')
        
        self.category = Category.objects.create(name='Movies')
        
        # We need a dummy file for streaming tests
        test_file_path = os.path.join(settings.BASE_DIR, 'protected_media', 'test_video.mp4')
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        with open(test_file_path, 'wb') as f:
            f.write(b"dummy video content")
            
        self.media_free = MediaAsset.objects.create(
            title='Free Video',
            description='Free content',
            category=self.category,
            creator=self.creator,
            publication_status='PUBLISHED',
            is_premium=False,
            media_file='test_video.mp4'
        )
        
        self.media_premium = MediaAsset.objects.create(
            title='Premium Video',
            description='Premium content',
            category=self.category,
            creator=self.creator,
            publication_status='PUBLISHED',
            is_premium=True,
            media_file='test_video.mp4'
        )
        
        self.media_draft = MediaAsset.objects.create(
            title='Draft Video',
            description='Draft content',
            category=self.category,
            creator=self.creator,
            publication_status='DRAFT',
            is_premium=False,
            media_file='test_video.mp4'
        )

        self.plan = SubscriptionPlan.objects.create(name='Pro', price=10.0, duration_days=30)

    def tearDown(self):
        test_file_path = os.path.join(settings.BASE_DIR, 'protected_media', 'test_video.mp4')
        if os.path.exists(test_file_path):
            try:
                os.remove(test_file_path)
            except OSError:
                pass

    def test_premium_requires_subscription(self):
        self.client.login(username='subscriber', password='password')
        url = reverse('catalog:generate_token', args=[self.media_premium.pk])
        response = self.client.get(url)
        # Should be forbidden because no active subscription
        self.assertEqual(response.status_code, 403)

    def test_authorized_token_generation_premium(self):
        # Give subscriber a subscription
        Subscription.objects.create(
            user=self.subscriber, plan=self.plan, 
            end_date=timezone.now() + timedelta(days=10), is_active=True
        )
        
        self.client.login(username='subscriber', password='password')
        url = reverse('catalog:generate_token', args=[self.media_premium.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_expired_subscription_cannot_stream(self):
        Subscription.objects.create(
            user=self.subscriber, plan=self.plan, 
            end_date=timezone.now() - timedelta(days=1), is_active=True
        )
        
        self.client.login(username='subscriber', password='password')
        url = reverse('catalog:generate_token', args=[self.media_premium.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_stream_valid_token(self):
        key = AccessKey.objects.create(
            user=self.subscriber,
            media_asset=self.media_free,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        
        url = reverse('catalog:stream_media', args=[key.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check if streaming record was created
        self.assertTrue(StreamingRecord.objects.filter(user=self.subscriber, media_asset=self.media_free).exists())

    def test_invalid_access_token_is_rejected(self):
        # Fake UUID token
        url = reverse('catalog:stream_media', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_expired_token_is_rejected(self):
        key = AccessKey.objects.create(
            user=self.subscriber,
            media_asset=self.media_free,
            expires_at=timezone.now() - timedelta(hours=1)
        )
        url = reverse('catalog:stream_media', args=[key.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_unpublished_media_cannot_be_streamed(self):
        # Even with a valid token, if media status changes to draft, stream should be rejected
        key = AccessKey.objects.create(
            user=self.subscriber,
            media_asset=self.media_draft,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        url = reverse('catalog:stream_media', args=[key.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_creator_dashboard_access(self):
        self.client.login(username='subscriber', password='password')
        url = reverse('catalog:creator_dashboard')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        
        self.client.login(username='creator', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_watch_history(self):
        self.client.login(username='subscriber', password='password')
        url = reverse('catalog:update_progress', args=[self.media_free.pk])
        response = self.client.post(url, {'progress': 120})
        self.assertEqual(response.status_code, 200)
        
        history = WatchHistory.objects.get(user=self.subscriber, media_asset=self.media_free)
        self.assertEqual(history.progress_seconds, 120)


    def test_media_detail(self):
        url = reverse('catalog:media_detail', args=[self.media_free.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Free Video')

    def test_creator_can_publish_media(self):
        self.client.login(username='creator', password='password')
        self.media_draft.publication_status = 'PUBLISHED'
        self.media_draft.save()
        url = reverse('catalog:media_detail', args=[self.media_draft.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
