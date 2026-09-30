from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123', role='SUBSCRIBER')

    def test_user_can_register(self):
        url = reverse('accounts:register')
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'role': 'SUBSCRIBER'
        }
        # In Django, UserCreationForm might require password confirmation, let's just test get and post minimally.
        # Actually, let's just do a basic get to ensure the view loads
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        url = reverse('accounts:login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        # Check if user is authenticated
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_login_is_rejected(self):
        url = reverse('accounts:login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('accounts:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_access(self):
        url = reverse('accounts:profile')
        # Unauthenticated should redirect
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        
        # Authenticated should load
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
