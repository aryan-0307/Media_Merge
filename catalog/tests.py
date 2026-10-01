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

from .models import MovieDatasetRecord

class MovieDatabaseTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        # Create a small test dataset instead of 50k
        for i in range(1, 31):
            MovieDatasetRecord.objects.create(
                source_id=f"test_id_{i}",
                title=f"Test Movie {i} money",
                original_title=f"Original Test Movie {i}",
                media_type="Movie",
                release_year=2000 + (i % 5),  # 2000, 2001, 2002, 2003, 2004
                runtime_minutes=120,
                language="hindi" if i % 2 == 0 else "tamil",
                genre="Action" if i % 3 == 0 else "Comedy",
                rating=8.0 + (i % 10) / 10.0,
                vote_count=100 * i,
                description="Test description"
            )

    def test_movie_database_list_status(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_movie_database_pagination(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 24)
        
        response_page2 = self.client.get(url + "?page=2")
        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(len(response_page2.context['page_obj']), 6) # 30 total, 24 on p1, 6 on p2

    def test_movie_database_search(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url, {'q': 'Test Movie 1'})
        self.assertEqual(response.status_code, 200)
        # 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
        self.assertTrue(len(response.context['page_obj']) > 0)
        self.assertContains(response, "Test Movie 1")

    def test_movie_database_language_filter(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url, {'language': 'hindi'})
        self.assertEqual(response.status_code, 200)
        # Should only contain hindi movies (evens)
        for record in response.context['page_obj']:
            self.assertEqual(record.language, 'hindi')

    def test_movie_database_genre_filter(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url, {'genre': 'Action'})
        self.assertEqual(response.status_code, 200)
        for record in response.context['page_obj']:
            self.assertEqual(record.genre, 'Action')

    def test_movie_database_year_filter(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url, {'year': '2001'})
        self.assertEqual(response.status_code, 200)
        for record in response.context['page_obj']:
            self.assertEqual(record.release_year, 2001)

    def test_movie_database_sorting(self):
        url = reverse('catalog:movie_database_list')
        response = self.client.get(url, {'sort': 'rating_desc'})
        self.assertEqual(response.status_code, 200)
        records = list(response.context['page_obj'])
        # Check if sorted by rating desc
        for i in range(len(records) - 1):
            if records[i].rating and records[i+1].rating:
                self.assertTrue(records[i].rating >= records[i+1].rating)

    def test_movie_database_detail(self):
        movie = MovieDatasetRecord.objects.first()
        url = reverse('catalog:movie_database_detail', args=[movie.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, movie.title)
        self.assertContains(response, "Metadata Record")
        self.assertContains(response, "not directly streamable")

    def test_invalid_movie_detail(self):
        url = reverse('catalog:movie_database_detail', args=[999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

