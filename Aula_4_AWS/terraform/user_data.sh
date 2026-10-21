#!/bin/bash
# Executado uma única vez no primeiro boot da instância (log em /var/log/cloud-init-output.log)
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

# --- Docker Engine + Compose plugin (repositório oficial) ---
apt-get update
apt-get install -y ca-certificates curl git rsync
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable --now docker
usermod -aG docker ubuntu

# Permite usar "docker-compose" (sintaxe do LEIAME) além de "docker compose"
cat > /usr/local/bin/docker-compose <<'EOF'
#!/bin/sh
exec docker compose "$@"
EOF
chmod +x /usr/local/bin/docker-compose

# --- Swap de 8 GB (a instância Free Tier tem só 8 GB de RAM) ---
fallocate -l 8G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile none swap sw 0 0" >> /etc/fstab
echo "vm.swappiness=10" > /etc/sysctl.d/99-swap.conf

# --- Requisito do Elasticsearch ---
echo "vm.max_map_count=262144" > /etc/sysctl.d/99-elasticsearch.conf
sysctl --system

touch /home/ubuntu/.docker-pronto
