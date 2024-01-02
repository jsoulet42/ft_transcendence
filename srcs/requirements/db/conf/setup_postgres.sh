#!/bin/bash
set -e

# Script pour configurer la base de données PostgreSQL dans Docker

# Attendre que le serveur PostgreSQL démarre
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"
do
  echo "En attente de la disponibilité de PostgreSQL..."
  sleep 2
done

# Créer la base de données et les utilisateurs
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE api42;
    CREATE USER $PG_USER WITH PASSWORD '$PG_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE api42 TO $PG_USER;
EOSQL

echo "Configuration de la base de données terminée."
