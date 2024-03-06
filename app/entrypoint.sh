#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
	echo "Waiting for postgres..."

	while ! nc -z $DJANGO_PG_HOST $DJANGO_PG_PORT; do
		sleep 0.1
	done

	echo "PostgreSQL started"
fi

#python manage.py flush --no-input

python manage.py makemigrations backend
python manage.py makemigrations friends
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --no-input

exec "$@"
