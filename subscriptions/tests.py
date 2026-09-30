from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import SubscriptionPlan, Subscription

User = get_user_model()

class SubscriptionsTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123', role='SUBSCRIBER')
        self.plan = SubscriptionPlan.objects.create(
            name='Premium', price=9.99, duration_days=30, is_active=True
        )

    def test_plan_list_view(self):
        url = reverse('subscriptions:plans')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Premium')

    def test_subscribe_view(self):
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('subscriptions:subscribe', args=[self.plan.id])
        # Suppose a POST creates a subscription
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) # Redirects on success
        
        # Verify subscription was created
        self.assertTrue(Subscription.objects.filter(user=self.user, plan=self.plan).exists())
        sub = Subscription.objects.get(user=self.user, plan=self.plan)
        self.assertTrue(sub.is_valid())

    def test_expired_subscription(self):
        # Create an expired subscription manually
        sub = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=timezone.now() - timedelta(days=60),
            end_date=timezone.now() - timedelta(days=30),
            is_active=True
        )
        self.assertFalse(sub.is_valid())
