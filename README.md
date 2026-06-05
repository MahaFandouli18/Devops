# 📝 Todo App — DevOps Assessment

Application three-tier containerisée avec pipeline CI/CD complet.

## 🏗️ Architecture
## ⚡ Démarrage rapide

### Prérequis
- Docker >= 24.0
- Docker Compose plugin

### Lancer en local

```bash
git clone https://github.com/MahaFandouli18/Devops.git
cd Devops
cp .env.example .env
docker compose up --build
```

| Service    | URL                        |
|------------|----------------------------|
| Frontend   | http://localhost:8080      |
| API        | http://localhost:5000      |
| Monitoring | http://localhost:3001      |

## 🔐 Secrets

Ne jamais commiter le fichier `.env`. Copie `.env.example` :

```bash
cp .env.example .env
```

Le pipeline CI/CD utilise les GitHub Secrets :
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## 🔄 Pipeline CI/CD

Sur chaque push :
1. **Lint** — flake8 sur le code Python
2. **Validate** — docker compose config
3. **Build & Push** — images vers Docker Hub
4. **Deploy** — sur branche main

## ✅ Health Checks

- API : `GET /health` → `{"status": "ok", "db": "connected"}`
- Frontend : `GET /health` → `frontend ok`

## 🛠️ Scripts

```bash
# Déployer
./scripts/deploy.sh

# Backup MongoDB
./scripts/backup-db.sh
```
