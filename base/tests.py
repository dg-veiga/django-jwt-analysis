from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Create your tests here.

class MyTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def _create_simple_user(self):
        user = User.objects.create_user(username='user_001', email='user_001@example.com', password='user_001_password', is_active=True)
        user.save()

    def test__unauthorized_acess__expected_error_401(self):
        c = Client()
        response = c.get('/api/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])

    def test__authorized_acess_with_token__expected_success(self):
        self._create_simple_user()

        user = User.objects.get(username='user_001')
        user.refresh_from_db()

        response = self.client.post('/api/token/', {
            "username": "user_001",
            "password": "user_001_password"
        })

        json_response = response.json()

        self.assertFalse(json_response.get('refresh', False) == False)
        self.assertFalse(json_response.get('access', False) == False)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + json_response['access'])
        response_2 = client.get('/api/', data={'format': 'json'})

        json_response_2 = response_2.json()

        self.assertEqual(200, response_2.status_code)
        self.assertEqual('success', json_response_2['msg'])
