# Utiliser l'image officielle de Kibana
FROM docker.elastic.co/kibana/kibana:latest

# Copier le script de configuration depuis le répertoire conf
COPY conf/setup_kibana.sh /usr/share/kibana/

# Rendre le script exécutable
RUN chmod +x /usr/share/kibana/setup_kibana.sh

# Exposer le port par défaut de Kibana
EXPOSE 5601

# Démarrer Kibana en utilisant le script de configuration
CMD ["/usr/share/kibana/setup_kibana.sh"]
