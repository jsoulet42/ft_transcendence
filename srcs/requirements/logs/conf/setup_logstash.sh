#!/bin/bash
set -e

# Configurer les permissions du répertoire de données
chown -R logstash:logstash /usr/share/logstash/data

# Démarrer Logstash
exec /usr/share/logstash/bin/logstash
