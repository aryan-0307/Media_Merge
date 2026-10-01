from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from catalog.models import MediaAsset, Category, AccessKey, MovieDatasetRecord
from subscriptions.models import Subscription, SubscriptionPlan
from analytics.models import StreamingRecord, WatchHistory
from royalties.models import RoyaltyRecord

User = get_user_model()

class Rigorous100UsersTest(TransactionTestCase):
    def setUp(self):
        # We need some initial data to interact with
        self.category = Category.objects.create(name='Movies')
        self.creator = User.objects.create_user(username='creator_master', password='password', role='CREATOR')
        
        self.media_free = MediaAsset.objects.create(
            title='Free Master Video',
            description='Free content',
            category=self.category,
            creator=self.creator,
            publication_status='PUBLISHED',
            is_premium=False,
        )
        self.media_premium = MediaAsset.objects.create(
            title='Premium Master Video',
            description='Premium content',
            category=self.category,
            creator=self.creator,
            publication_status='PUBLISHED',
            is_premium=True,
        )
        
        # Test Subscription Plan
        self.plan = SubscriptionPlan.objects.create(name='Pro Test', price=10.0, duration_days=30)
        
        # We'll create exactly 100 users, but maybe we do it in the test itself to trace errors.

    def test_100_users_workflow(self):
        errors_encountered = []
        
        for i in range(1, 101):
            username = f'testuser{i:03d}'
            password = 'password123'
            
            try:
                # 1. Registration
                user = User.objects.create_user(username=username, password=password, role='SUBSCRIBER')
                
                client = Client()
                
                # 2. Login
                login_success = client.login(username=username, password=password)
                if not login_success:
                    raise Exception(f"Login failed for {username}")
                
                # 3. Profile Access
                response = client.get(reverse('accounts:profile'))
                if response.status_code != 200:
                    raise Exception(f"Profile access failed for {username}. Status: {response.status_code}")
                
                # 4. Movie Database interactions
                # Search
                search_term = 'test' if i % 2 == 0 else 'money'
                response = client.get(reverse('catalog:movie_database_list') + f'?q={search_term}')
                if response.status_code != 200:
                    raise Exception(f"Movie database search failed for {username}")
                
                # Filter & Sort
                response = client.get(reverse('catalog:movie_database_list') + '?language=hindi&sort=rating_desc')
                if response.status_code != 200:
                    raise Exception(f"Movie database filter/sort failed for {username}")
                
                # Check pagination
                response = client.get(reverse('catalog:movie_database_list') + '?page=2')
                if response.status_code not in [200, 404]: # 404 might happen if there are less than 2 pages in db
                    raise Exception(f"Movie database pagination failed for {username}. Status: {response.status_code}")
                
                # 5. Subscribe (For some users)
                if i % 3 == 0:
                    # Give them a subscription
                    Subscription.objects.create(
                        user=user, plan=self.plan, 
                        end_date=timezone.now() + timedelta(days=30), is_active=True
                    )
                    
                    # Try accessing premium content
                    response = client.get(reverse('catalog:generate_token', args=[self.media_premium.pk]))
                    if response.status_code != 200:
                        raise Exception(f"Subscribed user {username} could not access premium content")
                else:
                    # Try accessing premium content (should fail)
                    response = client.get(reverse('catalog:generate_token', args=[self.media_premium.pk]))
                    if response.status_code != 403:
                        raise Exception(f"Unsubscribed user {username} accessed premium content! Status: {response.status_code}")
                
                # 6. Access free content
                response = client.get(reverse('catalog:generate_token', args=[self.media_free.pk]))
                if response.status_code != 200:
                    raise Exception(f"User {username} could not access free content")
                    
                # The token generation triggers token creation
                token_data = response.json()
                if 'token' not in token_data:
                    raise Exception(f"No token received for {username}")
                
                token = token_data['token']
                
                # Attempt stream (simulate file request)
                # Since no media file exists, it will raise 404 which is expected, but the record should be created.
                response = client.get(reverse('catalog:stream_media', args=[token]))
                if response.status_code not in [200, 404]: # 404 is because file is missing, but auth passed
                    raise Exception(f"Stream media endpoint failed for {username}. Status: {response.status_code}")
                
                # Wait, stream_media records streaming start. Let's check record.
                has_record = StreamingRecord.objects.filter(user=user, media_asset=self.media_free).exists()
                if not has_record:
                    raise Exception(f"Streaming record not created for {username}")
                
                # Test unauthorized access
                client.logout()
                response = client.get(reverse('accounts:profile'))
                if response.status_code != 302: # Redirect to login
                    raise Exception(f"Logged out user {username} could access profile")
                
            except Exception as e:
                errors_encountered.append({
                    'user': username,
                    'error': str(e)
                })
        
        # 7. Process Royalties and verify creator earnings
        from royalties.services import calculate_royalties
        calculate_royalties()
        
        # Verify royalties
        earnings = RoyaltyRecord.objects.filter(creator=self.creator).count()
        print(f"Generated {earnings} royalty records for the creator.")
        self.assertTrue(earnings > 0, "No royalties were calculated despite streaming activity.")
        
        if errors_encountered:
            print("\nERRORS ENCOUNTERED:")
            for err in errors_encountered:
                print(f"- {err['user']}: {err['error']}")
            
        self.assertEqual(len(errors_encountered), 0, f"Encountered {len(errors_encountered)} errors during 100-user workflow test.")
        print(f"Successfully processed {100 - len(errors_encountered)}/100 users without workflow errors.")
