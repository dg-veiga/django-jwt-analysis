# django-jwt-workaround
## How to run:
DJANGO APP:
```sh
git clone *project*
cd *project*
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8008
```

## Routes:
GET /api/index
```json
RESPONSE
{
    "msg": "success"
}
```
POST /insert
```json
PAYLOAD
{

}
```

Observations:
- django port: 8008
- Superuser:
    - username: admin
    - password: admin
    - email: admin@example.com
