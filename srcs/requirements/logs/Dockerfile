# Utiliser l'image officielle de Logstash
FROM docker.elastic.co/logstash/logstash:latest

# Copier le script de configuration depuis le répertoire conf
COPY conf/setup_logstash.sh /usr/share/logstash/

# Rendre le script exécutable
RUN chmod +x /usr/share/logstash/setup_logstash.sh

# Exposer les ports par défaut de Logstash
EXPOSE 9600 5000

# Démarrer Logstash en utilisant le script de configuration
CMD ["/usr/share/logstash/setup_logstash.sh"]
