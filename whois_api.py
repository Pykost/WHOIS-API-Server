#!/usr/bin/env python3
# whois_api.py
# Simple Flask WHOIS API with JSON and HTML endpoints.
# Designed to be run with gunicorn in production (systemd unit uses gunicorn).

from flask import Flask, request, jsonify, render_template_string
import whois
import tldextract
import logging

app = Flask(__name__)

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whois_api")

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>WHOIS for {{ target }}</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background:#f7f7f7; }
    .card { background:#fff; padding:16px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
    pre { white-space: pre-wrap; word-wrap: break-word; }
    h1 { margin-top:0; font-size:20px; }
    .meta { color:#555; font-size:13px; margin-bottom:10px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>WHOIS for {{ target }}</h1>
    <div class="meta">Type: {{ kind }} &nbsp;|&nbsp; Raw fields shown below</div>
    <pre>{{ data }}</pre>
  </div>
</body>
</html>
"""

def normalize_query(q: str) -> str:
    return q.strip()

def guess_kind(q: str) -> str:
    # crude check: IP if only digits and dots, else domain if tldextract finds a suffix
    if all(ch.isdigit() or ch == '.' for ch in q):
        return "IP"
    ext = tldextract.extract(q)
    return "Domain" if ext.suffix else "Unknown"

def whois_safe_lookup(target: str):
    try:
        w = whois.whois(target)
        # whois.whois returns dict-like; convert to JSON-serializable
        result = {}
        # some keys are attributes; iterate in safe manner
        try:
            items = dict(w)
        except Exception:
            # fallback: stringify entire object
            return {"raw": str(w)}
        for k, v in items.items():
            # convert objects/lists to JSON-friendly representation
            try:
                # Many whois fields are lists/strings/datetimes - letting flask/json handle them
                result[k] = v
            except Exception:
                result[k] = str(v)
        return result
    except Exception as e:
        # bubble up error message
        raise

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/whois")
def whois_json():
    target = request.args.get("query") or request.args.get("q")
    if not target:
        return jsonify({"error": "Missing query parameter 'query' or 'q'"}), 400
    target = normalize_query(target)
    kind = guess_kind(target)
    try:
        result = whois_safe_lookup(target)
        logger.info("WHOIS JSON lookup %s", target)
        return jsonify({"query": target, "kind": kind, "result": result})
    except Exception as e:
        logger.exception("WHOIS lookup failed for %s", target)
        return jsonify({"error": str(e)}), 500

@app.route("/whois/html")
def whois_html():
    target = request.args.get("query") or request.args.get("q")
    if not target:
        return "Missing query parameter 'query' or 'q'", 400
    target = normalize_query(target)
    kind = guess_kind(target)
    try:
        raw = whois_safe_lookup(target)
        # present readable text
        if isinstance(raw, dict):
            data_text = ""
            for k, v in raw.items():
                data_text += f"{k}: {v}\n"
        else:
            data_text = str(raw)
        logger.info("WHOIS HTML lookup %s", target)
        return render_template_string(HTML_TEMPLATE, target=target, data=data_text, kind=kind)
    except Exception as e:
        logger.exception("WHOIS HTML lookup failed for %s", target)
        return render_template_string(HTML_TEMPLATE, target=target, data=f"Error: {e}", kind=kind), 500

if __name__ == "__main__":
    # Debug server only for development/testing
    app.run(host="0.0.0.0", port=8080)

