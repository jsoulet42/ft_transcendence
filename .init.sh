#!/bin/bash

# give access by this command
# chmod +x init.sh

# Our hostname
DATA_DIR="/home/groot/data"

# FRONTEND
mkdir -p "$DATA_DIR/frontend"
find "$DATA_DIR/frontend" -type d -exec chmod 750 {} \;

mkdir -p "$DATA_DIR/backend"
find "$DATA_DIR/backend" -type d -exec chmod 750 {} \;

# BACKEND
mkdir -p "$DATA_DIR/backend"
find "$DATA_DIR/backend" -type d -exec chmod 750 {} \;

mkdir -p "$DATA_DIR/backend/api"
find "$DATA_DIR/backend/api" -type d -exec chmod 750 {} \;

mkdir -p "$DATA_DIR/backend/postgres"
find "$DATA_DIR/backend/postgres" -type d -exec chmod 750 {} \;

# DEVOPS
mkdir -p "$DATA_DIR/devops"
mkdir -p "$DATA_DIR/devops/elasticsearch"
chown -R 1000:1000 "$DATA_DIR/devops/elasticsearch"
find "$DATA_DIR/devops/elasticsearch" -type d -exec chmod 750 {} \;

mkdir -p "$DATA_DIR/devops/logstash"
chown -R 1000:1000 "$DATA_DIR/devops/logstash"

mkdir -p "$DATA_DIR/devops/kibana"
chown -R 1000:1000 "$DATA_DIR/devops/kibana"


