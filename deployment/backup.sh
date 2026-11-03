#!/usr/bin/env bash
# ========================================================
# CSE ASPIRANT – Automated Database & Cache Backup Script
# ========================================================

set -euo pipefail

BACKUP_DIR="/var/backups/cse-aspirant"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "${BACKUP_DIR}"

echo "[BACKUP] Starting PostgreSQL & Redis backup at ${TIMESTAMP}..."

# 1. PostgreSQL Backup
docker exec cse_postgres pg_dump -U cse_admin cse_aspirant | gzip > "${BACKUP_DIR}/pg_cse_aspirant_${TIMESTAMP}.sql.gz"
echo "[BACKUP] PostgreSQL dump saved: pg_cse_aspirant_${TIMESTAMP}.sql.gz"

# 2. Redis RDB Backup
docker exec cse_redis redis-cli save
docker cp cse_redis:/data/dump.rdb "${BACKUP_DIR}/redis_dump_${TIMESTAMP}.rdb"
echo "[BACKUP] Redis dump saved: redis_dump_${TIMESTAMP}.rdb"

# 3. Retention policy: Keep last 14 days of backups
find "${BACKUP_DIR}" -type f -mtime +14 -name "*.gz" -delete
find "${BACKUP_DIR}" -type f -mtime +14 -name "*.rdb" -delete

echo "[BACKUP] Backup completed successfully."

