# Utiliser l'image officielle de Caddy basée sur Alpine
FROM caddy:2.3.0-alpine

# Copier le script de configuration dans le conteneur
COPY conf/setup_caddy.sh /setup_caddy.sh

# Rendre le script exécutable
RUN chmod +x /setup_caddy.sh

# Exécuter le script au démarrage du conteneur
CMD ["/setup_caddy.sh"]

