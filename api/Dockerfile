# ── Étape 1 : builder (installe les dépendances) ──
FROM python:3.12-slim AS builder

WORKDIR /app

# Copier seulement requirements d'abord (optimise le cache Docker)
COPY requirements.txt .

# Installer dans un dossier isolé
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Étape 2 : image finale (légère) ──
FROM python:3.12-slim

WORKDIR /app

# Copier les dépendances installées
COPY --from=builder /install /usr/local

# Copier le code
COPY app.py .

# Créer un utilisateur non-root (sécurité)
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
