import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from decimal import Decimal

from catalog.models import Category, MediaAsset
from subscriptions.models import SubscriptionPlan, Subscription
from analytics.models import StreamingRecord, WatchHistory
from royalties.models import RoyaltyRate
from royalties.services import calculate_royalties

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds realistic demo data into MediaMerge'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting seed process...")
        random.seed(42) # Deterministic randomness where possible

        # 1. Users
        self.stdout.write("Seeding Users...")
        admin, _ = User.objects.get_or_create(username='demo_admin', defaults={'role': 'ADMIN', 'email': 'admin@mediamerge.demo'})
        if _:
            admin.set_password('demo_admin123')
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
        
        creators = []
        for i in range(1, 6):
            creator, created = User.objects.get_or_create(username=f'demo_creator_{i}', defaults={'role': 'CREATOR', 'email': f'creator{i}@mediamerge.demo'})
            if created:
                creator.set_password('demo_creator123')
                creator.save()
            creators.append(creator)
            
        subscribers = []
        for i in range(1, 16):
            subscriber, created = User.objects.get_or_create(username=f'demo_sub_{i}', defaults={'role': 'SUBSCRIBER', 'email': f'sub{i}@mediamerge.demo'})
            if created:
                subscriber.set_password('demo_sub123')
                subscriber.save()
            subscribers.append(subscriber)
            
        # 2. Categories
        self.stdout.write("Seeding Categories...")
        categories = []
        category_names = ['Action', 'Drama', 'Comedy', 'Documentary', 'Sci-Fi', 'Thriller', 'Animation', 'Sports']
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': f'{name} movies and shows.'})
            categories.append(cat)
            
        # 3. Subscription Plans
        self.stdout.write("Seeding Subscription Plans...")
        plans_data = [
            {'name': 'Free', 'price': '0.00', 'duration_days': 30, 'description': 'Ad-supported basic access.'},
            {'name': 'Basic', 'price': '99.00', 'duration_days': 30, 'description': 'Standard Definition access.'},
            {'name': 'Standard', 'price': '199.00', 'duration_days': 30, 'description': 'High Definition access.'},
            {'name': 'Premium', 'price': '299.00', 'duration_days': 30, 'description': '4K HDR access.'},
        ]
        plans = []
        for p in plans_data:
            plan, _ = SubscriptionPlan.objects.get_or_create(name=p['name'], defaults={
                'price': Decimal(p['price']),
                'duration_days': p['duration_days'],
                'description': p['description']
            })
            plans.append(plan)
            
        # 4. Media Assets
        self.stdout.write("Seeding Media Assets...")
        demo_media = MediaAsset.objects.filter(title__startswith='Demo:')
        if demo_media.count() < 30:
            for i in range(30):
                creator = random.choice(creators)
                category = random.choice(categories)
                title = f'Demo: Realistic {category.name} Title {i+1}'
                
                if not MediaAsset.objects.filter(title=title).exists():
                    asset = MediaAsset(
                        title=title,
                        description=f'This is a realistic description for {title}. A compelling story in the {category.name} genre.',
                        media_type='VIDEO',
                        category=category,
                        language=random.choice(['English', 'Hindi', 'Spanish', 'French']),
                        release_date=timezone.now().date() - timedelta(days=random.randint(10, 1000)),
                        duration=random.randint(120, 7200),
                        creator=creator,
                        publication_status='PUBLISHED',
                        is_premium=random.choice([True, False])
                    )
                    asset.media_file.save(f'demo_media_{i}.mp4', ContentFile(b'dummy content'), save=False)
                    asset.save()
            demo_media = MediaAsset.objects.filter(title__startswith='Demo:')
        else:
            self.stdout.write("Media assets already seeded.")
            
        # 5. Subscribers
        self.stdout.write("Seeding Subscriptions...")
        for subscriber in subscribers:
            if not Subscription.objects.filter(user=subscriber, is_active=True).exists():
                plan = random.choice(plans)
                Subscription.objects.create(
                    user=subscriber,
                    plan=plan,
                    start_date=timezone.now() - timedelta(days=random.randint(1, 20)),
                    end_date=timezone.now() + timedelta(days=random.randint(10, 30)),
                    is_active=True
                )
                
        # 6. Streaming Records
        self.stdout.write("Seeding Streaming Records...")
        if StreamingRecord.objects.filter(user__in=subscribers).count() < 75:
            media_list = list(demo_media)
            if media_list:
                for _ in range(100):
                    user = random.choice(subscribers)
                    # Non-uniform distribution
                    media = random.choice(media_list[:10] * 3 + media_list[10:]) 
                    # use slightly randomized time in the past
                    record = StreamingRecord.objects.create(
                        user=user,
                        media_asset=media,
                        royalty_processed=False
                    )
                    record.started_at = timezone.now() - timedelta(days=random.randint(0, 30))
                    record.save()
                    
        # 7. Watch History
        self.stdout.write("Seeding Watch History...")
        if WatchHistory.objects.filter(user__in=subscribers).count() < 40:
            media_list = list(demo_media)
            if media_list:
                count = 0
                for user in subscribers:
                    for _ in range(random.randint(2, 5)):
                        media = random.choice(media_list)
                        if not WatchHistory.objects.filter(user=user, media_asset=media).exists():
                            WatchHistory.objects.create(
                                user=user,
                                media_asset=media,
                                progress_seconds=random.randint(10, media.duration or 300)
                            )
                            count += 1
                        if count >= 60:
                            break
                    if count >= 60:
                        break

        # 8. Royalties
        self.stdout.write("Setting up Royalties...")
        RoyaltyRate.objects.get_or_create(rate_per_stream=Decimal('0.5000'), is_active=True)
        
        self.stdout.write("Calculating Royalties...")
        result = calculate_royalties()
        self.stdout.write(f"Processed {result['records_created']} royalty records totaling INR {result['total_payout']}.")

        self.stdout.write(self.style.SUCCESS("Seed process completed successfully!"))
