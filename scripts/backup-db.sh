#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/tmp/mongo-backups}"
CONTAINER="${MONGO_CONTAINER:-todo-mongo}"
DB_NAME="${DB_NAME:-tododb}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/backup-$DB_NAME-$TIMESTAMP.gz"

mkdir -p "$BACKUP_DIR"

echo "[$(date +%H:%M:%S)] 📦 Backup de '$DB_NAME'..."

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "❌ Conteneur '$CONTAINER' non trouvé"; exit 1
fi

docker exec "$CONTAINER" mongodump \
  --db "$DB_NAME" --archive --gzip > "$BACKUP_FILE"

SIZE="$(du -sh "$BACKUP_FILE" | cut -f1)"
echo "[$(date +%H:%M:%S)] ✅ Backup créé : $BACKUP_FILE ($SIZE)"

ls -t "$BACKUP_DIR"/backup-*.gz 2>/dev/null | tail -n +8 | xargs -r rm --
echo "[$(date +%H:%M:%S)] ✨ Done."
