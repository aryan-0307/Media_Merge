from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AnalyticsTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword', role='ADMIN')
        self.user = User.objects.create_user(username='subscriber', password='password', role='SUBSCRIBER')
        
    def test_admin_dashboard_loads_for_admin(self):
        self.client.login(username='admin', password='adminpassword')
        url = reverse('analytics:admin_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_admin_dashboard_rejects_subscriber(self):
        self.client.login(username='subscriber', password='password')
        url = reverse('analytics:admin_dashboard')
        response = self.client.get(url)
        # Assuming user_passes_test redirects to login with ?next=...
        self.assertEqual(response.status_code, 302)
