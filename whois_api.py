from flask import Flask, request, jsonify, Response
import whois
import tldextract

app = Flask(__name__)

@app.route("/whois/json")
def whois_json():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    try:
        domain_info = whois.whois(query)
        # Convert all values to strings for JSON serialization
        data = {k: str(v) for k, v in domain_info.items()}
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/whois/html")
def whois_html():
    query = request.args.get("query")
    if not query:
        return Response("<h3>Error: Missing 'query' parameter</h3>", mimetype="text/html")
    try:
        domain_info = whois.whois(query)
        html = f"<h2>WHOIS Lookup for {query}</h2><pre>{domain_info.text}</pre>"
        return Response(html, mimetype="text/html")
    except Exception as e:
        return Response(f"<h3>Error: {e}</h3>", mimetype="text/html")

@app.route("/")
def home():
    return jsonify({"message": "WHOIS API is running", "endpoints": ["/whois/json", "/whois/html"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
