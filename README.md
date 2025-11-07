# WHOIS API

A simple Flask-based WHOIS lookup API that can be integrated into QRadar right-click menus.

## Endpoints

- `/whois/json?query=<domain>` — returns WHOIS info in JSON
- `/whois/html?query=<domain>` — returns WHOIS info in HTML

## Run locally
```bash
pip install -r requirements.txt
python3 whois_api.py


---

## 🧭 Step 3 — Push to GitHub

1. Open **Git Bash** (or VS Code Terminal).  
2. Go to your local folder:
   ```bash
   cd path/to/your/whois-api
