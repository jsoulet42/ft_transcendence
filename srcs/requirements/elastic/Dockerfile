# Utiliser l'image officielle d'Elasticsearch
FROM docker.elastic.co/elasticsearch/elasticsearch:7.16.2

# Copier le script de configuration depuis le répertoire conf
COPY conf/setup_elastic.sh /usr/share/elasticsearch/

# Rendre le script exécutable
RUN chmod +x /usr/share/elasticsearch/setup_elastic.sh

# Exposer les ports par défaut d'Elasticsearch
EXPOSE 9200 9300

# Démarrer Elasticsearch en utilisant le script de configuration
CMD ["/usr/share/elasticsearch/setup_elastic.sh"]

