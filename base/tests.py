from freezegun import freeze_time
from datetime import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient

# Create your tests here.

class MyTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.responses = {
            '401 Unauthorized - Token not valid': {
                "detail": "Given token not valid for any token type",
                "code": "token_not_valid",
                "messages": [
                    {
                        "token_class": "AccessToken",
                        "token_type": "access",
                        "message": "Token is invalid or expired"
                    }
                ]
            }
        }

    def _create_simple_user(self):
        user = User.objects.create_user(username='user_001', email='user_001@example.com', password='user_001_password', is_active=True)
        user.save()

    def test__unauthorized_access__expected_error_401(self):
        c = Client()
        response = c.get('/api/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])

    def test__authorized_access_with_token__expected_success(self):
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

    def test__access_not_authorized_with_expired_token__expected_error_401(self):
        self._create_simple_user()

        token = None

        with freeze_time("2021-01-01 12:00:00"):
            response = self.client.post('/api/token/', {
                "username": "user_001",
                "password": "user_001_password"
            })

            json_response = response.json()
            token = json_response['access']

            self.assertFalse(json_response.get('refresh', False) == False)
            self.assertFalse(json_response.get('access', False) == False)

        # settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] is set to 5 minutes
        with freeze_time("2021-01-01 12:06:00"):
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            response_2 = client.get('/api/', data={'format': 'json'})

            json_response_2 = response_2.json()

            self.assertEqual(401, response_2.status_code)
            self.assertEqual(self.responses['401 Unauthorized - Token not valid'], json_response_2)

    def test__access_authorized_with_still_valid_token__expected_success(self):
        self._create_simple_user()

        token = None

        with freeze_time("2021-01-01 12:00:00"):
            response = self.client.post('/api/token/', {
                "username": "user_001",
                "password": "user_001_password"
            })

            json_response = response.json()
            token = json_response['access']

            self.assertFalse(json_response.get('refresh', False) == False)
            self.assertFalse(json_response.get('access', False) == False)

        # settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] is set to 5 minutes
        with freeze_time("2021-01-01 12:04:00"):
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            response_2 = client.get('/api/', data={'format': 'json'})

            json_response_2 = response_2.json()

            self.assertEqual(200, response_2.status_code)
            self.assertEqual('success', json_response_2['msg'])

    def test__access_authorized_after_refresh_token__expected_success(self):
        self._create_simple_user()

        token = None
        refresh_token = None

        with freeze_time("2021-01-01 12:00:00"):
            response = self.client.post('/api/token/', {
                "username": "user_001",
                "password": "user_001_password"
            })

            json_response = response.json()
            token = json_response['access']
            refresh_token = json_response['refresh']

            self.assertFalse(json_response.get('refresh', False) == False)
            self.assertFalse(json_response.get('access', False) == False)

        # settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] is set to 5 minutes
        with freeze_time("2021-01-01 13:00:00"):
            response = self.client.post('/api/token/refresh/', {
                "refresh": refresh_token
            })

            json_response = response.json()
            token = json_response['access']

            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            response_2 = client.get('/api/', data={'format': 'json'})

            json_response_2 = response_2.json()

            self.assertEqual(200, response_2.status_code)
            self.assertEqual('success', json_response_2['msg'])

    def test__token_refresh_unauthorized_after_refresh_token_is_expired__expected_failure(self):
        self._create_simple_user()

        token = None
        refresh_token = None

        with freeze_time("2021-01-01 12:00:00"):
            response = self.client.post('/api/token/', {
                "username": "user_001",
                "password": "user_001_password"
            })

            json_response = response.json()
            token = json_response['access']
            refresh_token = json_response['refresh']

            self.assertFalse(json_response.get('refresh', False) == False)
            self.assertFalse(json_response.get('access', False) == False)

        # settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] is set to 1 day
        with freeze_time("2021-01-02 12:01:00"):
            response = self.client.post('/api/token/refresh/', {
                "refresh": refresh_token
            })

            json_response = response.json()

            self.assertEqual(401, response.status_code)
            self.assertEqual('Token is invalid or expired', json_response['detail'])
            self.assertEqual('token_not_valid', json_response['code'])
