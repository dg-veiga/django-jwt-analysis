from email import header
import json
from wsgiref import headers
from django.test import TestCase, Client
from django.contrib.auth.models import User
from mock import MagicMock, patch

# Create your tests here.

class MyTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def _create_simple_user(self):
        User.objects.create_user(username='user_001', email='user_001@example.com', password='user_001_password', is_active=True)        

    def test__unauthorized_acess__expected_error_401(self):
        c = Client()
        response = c.get('/api/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])

    def test__authorized_acess_with_token__expected_success(self):
        self._create_simple_user()

        c = Client()
        response = c.post('/api/token/', {
            "username": "user_001",
            "password": "user_001_password"
        })

        json_response = response.json()

        self.assertFalse(json_response.get('refresh', False) == False)
        self.assertFalse(json_response.get('access', False) == False)

        header={'Authorization': f"Bearer {json_response['access']}"}
        response = c.get('/api/', **header)

        self.assertEqual(200, response.status_code)
        self.assertEqual('success', response.json()['msg'])
