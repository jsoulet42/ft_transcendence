#!/bin/bash
set -e

# Configurer les permissions du répertoire de données
chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

# Démarrer Elasticsearch
exec /usr/share/elasticsearch/bin/elasticsearch

