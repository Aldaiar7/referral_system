# Referral system

Users can generate referral codes to share.

## Table of Contents

* [Setup](#setup)

## Setup


create .env file 

Inside .env file write
```
SECRET_KEY=your_key
DEBUG=false_for_production
ALLOWED_HOSTS=set_your_domain
EMAIL_HOST=your_smtp_host
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
SQL_ENGINE=use_postgres
SQL_HOST=db
SQL_PORT=port_of_your_postgres
POSTGRES_NAME=name_of_postgres
POSTGRES_USER=username_of_postgres
POSTGRES_PASSWORD=password_of_postgres

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

Use postgresql for database



Create .env.db file (env file for database)

Inside .env.db file write

```
POSTGRES_DB=name
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_PORT=port
POSTGRES_HOST=db
```

host should be db because we will connect to db service in docker container.

to start app with docker-compose use this command.

```
docker-compose up --build
```


to create superuser use next command.

container_id is id of your docker container.
```
docker exec -it container_id python manage.py createsuperuser
```
Admin will have 5 referral codes.

Go to admin panel and in periodic tasks and create a new task.

name for task is count-points

in task(registered) choose core.tasks.count_points

if there no registered tasks. 
in custom write core.tasks.count_points
create interval schedule set interval you want to points to be refreshed.

And you are good to go



 
