# Project_GILDI

multi-container flask application with Postgres as the database fronted by the nginx reverse proxy.

requires docker, docker-compose to be installed with an active internet connection.

## Steps to setup the environment

1. Bootstrap the DB
```bash
# you can skip this step for now but the signup system will fail and anything else that requires the database to function will fail.
$ docker-compose up -d db
$ docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
```

2. Generating self signed ssl_certificate.
```bash
cd conf.d
openssl req -subj '/CN=localhost' -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
```

3. Modify the env_file add your api keys. 
```bash
$ cd ..
$ vi env_file
```

4. Bring up the project
```bash
$ docker-compose up -d
# Run without -d to see debug console
```

5. https://hostIP to access the running project.


