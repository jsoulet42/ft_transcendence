#!/bin/bash
set -e

# Configurer les permissions du répertoire de données
chown -R kibana:kibana /usr/share/kibana/data

# Démarrer Kibana
exec /usr/share/kibana/bin/kibana
