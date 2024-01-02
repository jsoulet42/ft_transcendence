#!/bin/bash

# Chemin du répertoire de configuration de Caddy
CADDY_CONF_DIR="/etc/caddy"
CADDYFILE="$CADDY_CONF_DIR/Caddyfile"

# Créer le répertoire de configuration si nécessaire
mkdir -p "$CADDY_CONF_DIR"

# Créer ou remplacer le Caddyfile
cat << EOF > "$CADDYFILE"
transcendance.42.fr {
    reverse_proxy backend:3000
    encode gzip
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
}
EOF

# Démarrer Caddy
caddy run --config "$CADDYFILE" --adapter caddyfile
