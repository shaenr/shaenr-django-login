# shaenr-django-login

Use docker to run postgres db using the config in `settings.py`

## Docker Postgres Database

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

## Mail Server

Use `python -m smtpd -n -c DebuggingServer localhost:1025` to act as mail server for the password reset and account verification.