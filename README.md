# django-jwt-analysis

## How to run:

DJANGO API:

```sh
git clone *project*
cd *project*
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8000
```

TESTS:

```sh
python manage.py test
```

## Routes:

GET /api/

```json
RESPONSE
{
    "msg": "success"
}

ERROR 401 Unauthorized
{
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
```

POST /api/token/

```json
PAYLOAD
{
    "username": string,
    "password": string
}

RESPONSE
{
    "refresh": refresh token string,
    "access": access token string
}
```

POST /api/token/refresh/

```json
PAYLOAD
{
    "refresh": refresh token string
}

RESPONSE
{
    "access": new access token string
}
```

Observations:

- django port: 8000
- Superuser:
  - username: admin
  - password: admin
  - email: admin@example.com
