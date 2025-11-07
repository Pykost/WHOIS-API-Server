# WHOIS API

A simple Flask-based WHOIS lookup API that can be integrated into QRadar right-click menus.

## Endpoints

- `/whois/json?query=<domain>` — returns WHOIS info in JSON
- `/whois/html?query=<domain>` — returns WHOIS info in HTML

## Run locally
```bash
pip install -r requirements.txt
python3 whois_api.py
