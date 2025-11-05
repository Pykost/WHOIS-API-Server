# whois-api

Simple WHOIS API (Flask) with JSON and HTML endpoints. Designed to run behind systemd + gunicorn.

## Endpoints

- `GET /whois?query=example.com` -> JSON
- `GET /whois/html?query=example.com` -> human-friendly HTML
- `GET /health` -> basic health check

## Quick install on Ubuntu (commands to run on your VM)

Assumes you will clone repository to `/opt/whois-api`.

```bash
# 1) install prerequisites
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# 2) create service user
sudo useradd --system --no-create-home --shell /usr/sbin/nologin whoisapi

# 3) clone repository (change URL to your repo)
sudo git clone https://github.com/<your-user>/whois-api.git /opt/whois-api

# 4) set ownership
sudo chown -R $USER:$USER /opt/whois-api
sudo chown -R whoisapi:whoisapi /opt/whois-api  # you'll adjust before enabling service

# 5) create virtualenv and install
cd /opt/whois-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 6) set proper ownership (so systemd runs as whoisapi)
sudo chown -R whoisapi:whoisapi /opt/whois-api

# 7) copy systemd unit and enable
sudo cp etc/whois-api.service /etc/systemd/system/whois-api.service
sudo systemctl daemon-reload
sudo systemctl enable whois-api
sudo systemctl start whois-api
sudo systemctl status whois-api

# 8) firewall (if using ufw)
sudo ufw allow 8080/tcp
