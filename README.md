# Project_GILDI

multi-container flask application with Postgres as the database fronted by the nginx reverse proxy.

## Usage

1. Bootstrap the DB
```bash
$ docker-compose up -d db
$ docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
```

2. Bring up the project
```bash
$ docker-compose up -d
```

3. hostIP:8080 to access the running project.

4. Generating self signed ssl_certificate.
```bash
cd conf.d
openssl req -subj '/CN=localhost' -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
```
