#!/usr/bin/env bash
# ========================================================
# CSE ASPIRANT – Automated Linux VPS Setup & Installation
# ========================================================

set -euo pipefail

echo "=================================================="
echo "    CSE ASPIRANT - PRODUCTION INSTALLER"
echo "=================================================="

# 1. Update OS Packages
echo "[1/6] Updating system repositories..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl git ufw ffmpeg jq

# 2. Install Docker & Docker Compose
echo "[2/6] Verifying Docker engine..."
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER"
fi

# 3. Configure Firewall
echo "[3/6] Setting up UFW firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp
sudo ufw --force enable

# 4. Clone or Setup Workspace
INSTALL_DIR="/opt/cse-aspirant"
echo "[4/6] Configuring workspace in ${INSTALL_DIR}..."
sudo mkdir -p "${INSTALL_DIR}"
sudo chown -R "$USER":"$USER" "${INSTALL_DIR}"

if [ ! -f "${INSTALL_DIR}/.env" ]; then
    cp .env.example "${INSTALL_DIR}/.env"
    echo "Created .env file. Please edit with your BOT_TOKEN and credentials."
fi

# 5. Setup Systemd Service
echo "[5/6] Registering systemd daemon..."
sudo cp deployment/cse-aspirant.service /etc/systemd/system/cse-aspirant.service
sudo systemctl daemon-reload
sudo systemctl enable cse-aspirant.service

# 6. Build and Launch
echo "[6/6] Launching CSE Aspirant production stack..."
cd deployment
docker compose --env-file ../.env up -d --build

echo "=================================================="
echo "   CSE ASPIRANT SUCCESSFULLY DEPLOYED! 🚀"
echo "   API Docs: http://<VPS_IP>:8000/docs"
echo "   Dashboard: http://<VPS_IP>:3000"
echo "=================================================="

