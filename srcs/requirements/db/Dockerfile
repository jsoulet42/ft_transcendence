# Utiliser l'image officielle de PostgreSQL
FROM postgres:alpine

# Copier le script de configuration dans l'image
COPY conf/setup_postgres.sh /docker-entrypoint-initdb.d/setup_postgres.sh

# Rendre le script exécutable
RUN chmod +x /docker-entrypoint-initdb.d/setup_postgres.sh