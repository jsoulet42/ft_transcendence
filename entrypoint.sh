#!/bin/bash

# set -e

# if [ "$DATABASE" = "postgres" ]; then
#	 echo "Waiting for PostgreSQL..."

#	 while ! pg_isready -q -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
#		 sleep 3
#	 done

#	 echo "PostgreSQL started"

#	 # Créer l'utilisateur et lui accorder des autorisations
#	 psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
#		 CREATE USER "$POSTGRES_USER" WITH PASSWORD "$POSTGRES_PASSWORD";
#		 GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
# 	EOSQL
# fi

# python manage.py flush --no-input
# python manage.py migrate

# exec "$@"

if [ "$DATABASE" = "postgres" ]
then
	echo "Waiting for postgres..."

	while ! nc -z $DJANGO_PG_HOST $DJANGO_PG_PORT; do
		sleep 0.1
	done

	echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

python manage.py collectstatic --no-input

exec "$@"
