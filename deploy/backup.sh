#!/bin/sh
# Ежедневный бэкап базы. Поставить в cron на сервере:
#   0 3 * * * cd /opt/saqshy && sh deploy/backup.sh >> backups/backup.log 2>&1
set -e
mkdir -p backups
STAMP=$(date +%Y-%m-%d_%H%M)
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "backups/db_$STAMP.sql.gz"
# Храним 14 последних копий
ls -1t backups/db_*.sql.gz | tail -n +15 | xargs -r rm --
echo "OK $STAMP"
