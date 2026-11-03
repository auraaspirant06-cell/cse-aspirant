# CSE ASPIRANT – LINUX VPS DEPLOYMENT GUIDE

This guide provides instructions for deploying **CSE ASPIRANT** on Ubuntu/Debian Linux VPS instances.

## Prerequisites
- Linux VPS (Ubuntu 22.04 LTS or 24.04 LTS recommended)
- Minimum: 2 vCPU, 2 GB RAM, 20 GB SSD
- Recommended: 4 vCPU, 4 GB RAM (for concurrent high-bitrate audio streaming)
- Ports required: 80, 443, 8000, 3000

---

## Method 1: Automated VPS Setup Script

1. Clone or copy the `CSE-Aspirant` repository to `/opt/cse-aspirant`:
   ```bash
   sudo mkdir -p /opt/cse-aspirant
   sudo chown -R $USER:$USER /opt/cse-aspirant
   cp -r * /opt/cse-aspirant/
   ```

2. Make installer executable and run:
   ```bash
   cd /opt/cse-aspirant/deployment
   chmod +x install.sh backup.sh
   ./install.sh
   ```

3. The installer will:
   - Install Docker, Docker Compose, and FFmpeg.
   - Configure UFW firewall rules.
   - Copy `.env.example` to `.env`.
   - Setup and enable the `cse-aspirant.service` systemd daemon.
   - Build and start all 5 microservices in the background.

---

## Method 2: Manual Docker Compose Deployment

1. Navigate to deployment folder:
   ```bash
   cd deployment
   ```

2. Configure environment credentials:
   ```bash
   cd ..
   cp .env.example .env
   nano .env
   ```
   Provide the required values listed in [Environment Configuration](ENVIRONMENT.md), including Telegram, database, Redis, Go engine, security, and payment settings.

3. Launch the container stack:
   ```bash
   docker compose --env-file ../.env up -d --build
   ```

4. Verify services status:
   ```bash
   docker compose ps
   ```

---

## Method 3: Systemd Service Management

To control the bot service via systemd:
```bash
# Check status
sudo systemctl status cse-aspirant.service

# View live logs
sudo journalctl -u cse-aspirant.service -f

# Restart stack
sudo systemctl restart cse-aspirant.service
```

---

## Automated Backups

To set up daily automated database backups, add a cron job:
```bash
crontab -e
```
Add the following line (runs every day at 03:00 AM):
```cron
0 3 * * * /opt/cse-aspirant/deployment/backup.sh >> /var/log/cse-backup.log 2>&1
```
Backups are archived in `/var/backups/cse-aspirant` and automatically pruned after 14 days.

