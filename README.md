# Todo App — DevOps Assessment

Application three-tier containerisée avec pipeline CI/CD complet.

## Architecture
## Prérequis
- Docker >= 24.0
- Docker Compose plugin
- Git

## Démarrage rapide

```bash
git clone https://github.com/MahaFandouli18/Devops.git
cd Devops
cp .env.example .env
docker compose up --build
```

| Service      | URL                     |
|--------------|-------------------------|
| Frontend     | http://localhost:8080   |
| API          | http://localhost:5000   |
| Prometheus   | http://localhost:9090   |
| Grafana      | http://localhost:3000   |

## Secrets

Ne jamais commiter le fichier `.env`. Copie `.env.example` :

```bash
cp .env.example .env
# Remplis les valeurs
```

Le pipeline CI/CD utilise les GitHub Secrets :
- `DOCKERHUB_USERNAME` : ton username Docker Hub
- `DOCKERHUB_TOKEN` : ton token Docker Hub

## Pipeline CI/CD

Sur chaque push :
1. **Lint** — flake8 sur le code Python
2. **Validate** — docker compose config
3. **Build & Push** — images vers Docker Hub
4. **Deploy** — déclenché sur branche main

## Health Checks

- API : `GET /health` → `{"status": "ok", "db": "connected"}`
- Frontend : `GET /health` → `frontend ok`
- Prometheus : `http://localhost:9090`
- Grafana : `http://localhost:3000` (admin / voir .env)

## Métriques disponibles

L'API expose `/metrics` pour Prometheus :
- `http_requests_total` — nombre de requêtes par endpoint
- `http_request_duration_seconds` — latence des requêtes
- `todos_created_total` — nombre de todos créés

## Scripts

```bash
# Déployer
./scripts/deploy.sh

# Backup MongoDB
./scripts/backup-db.sh
```
