# shaenr-django-login


> REMEMBER: CHANGE THE `SECRET_KEY` AND `DEBUG = False` IN SETTINGS FILE BEFORE USING THIS IN PRODUCTION! 

---

### Custom User Model
Features a custom user model, manager and backend used for authentication.
+ Added fields: *email*, *date of birth*, and *email_verified*
+ Removed fields: *username*
+ Uses standard fields from `AbstractUser`
+ Will not create a new account without confirmed age over 18.
+ Non-authenticated Password reset (provide an email) + authenticated password change. Sends token to provided email.
+ Verify and confirm email address.

### Docker Postgres Database

Use docker to run postgres db using the config in `settings.py`

```bash
docker pull postgres
docker run 
    --name pg 
    -v /tmp/my-pgdata:/var/lib/postgresql/data 
    -e POSTGRES_PASSWORD=password 
    -p 127.0.0.1:5432:5432 
    -d postgres
```

From another shell...

```bash
docker exec -it pg su postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;"
```

### Mail Server

Use `python -m smtpd -n -c DebuggingServer localhost:1025` to act as mail server for the password reset and account verification.

### Django Setup

You'll need testing `django_project/.env` file:

```dotenv
NAME=postgres
USER=postgres
PASSWORD=password
HOST=127.0.0.1
PORT=5432
```

Then you can do:

```bash
python -m pip install -r requirements.txt
# Setup Postgres Database (see above)
python manage.py makemigrations
python manage.py migrate
python manage.py
python manage.py createsuperuser 
  --email admin@admin.com 
  --dob 1988-08-18 
  --email_verified True
# Run Mailserver Daemon in another Terminal (see above)
python manage.py runserver
```

### Working Endpoints
Just pulled from urls.py files.
So you can see what endpoints to test.

```python
    path('', include('shaenr_login.urls')),

    path('accounts/', shaenr_login_views.listing, name='listing'),
    path('accounts/profile/<int:_id>', shaenr_login_views.view_user, name='view_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("see_request/", shaenr_login_views.see_request),
    path('accounts/verify/confirm/', shaenr_login_views.get_verified, name='get_verified'),
    path('accounts/verify/<uidb64>/<token>', shaenr_login_views.verify_email, name='email_verify'),
    path('admin/', admin.site.urls),
```

---

### TODO

+ I should write some test cases and go from there...
+ I should implement a basic frontend layout...
+ I should write a logger.