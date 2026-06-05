#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()   { echo -e "${GREEN}[$(date +%H:%M:%S)] ✅ $*${NC}"; }
warn()  { echo -e "${YELLOW}[$(date +%H:%M:%S)] ⚠️  $*${NC}"; }
error() { echo -e "${RED}[$(date +%H:%M:%S)] ❌ $*${NC}"; exit 1; }

command -v docker >/dev/null 2>&1 || error "Docker non installé"
[ -f "$PROJECT_DIR/.env" ] || error "Fichier .env manquant"

cd "$PROJECT_DIR"

log "Arrêt de l'ancienne stack..."
docker compose down --remove-orphans

log "Démarrage de la nouvelle stack..."
docker compose up -d --build

log "Attente que les services démarrent..."
sleep 10

check_health() {
  local service="$1" url="$2"
  for i in $(seq 1 6); do
    if curl -sf "$url" > /dev/null 2>&1; then
      log "$service est healthy"; return 0
    fi
    warn "$service pas encore prêt ($i/6)..."; sleep 5
  done
  error "$service ne répond pas"
}

check_health "API"      "http://localhost:5000/health"
check_health "Frontend" "http://localhost:8080/health"

log "🎉 Déploiement réussi !"
echo ""
echo "  Frontend   → http://localhost:8080"
echo "  API        → http://localhost:5000"
echo "  Monitoring → http://localhost:3001"
