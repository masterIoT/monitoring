from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Ajoute le support pour CORS

# Route pour servir la page HTML
@app.route("/")
def index():
    return render_template("index.html")
# Route pour tester un service
@app.route("/check_service/<path:url>")
def check_service(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return jsonify({"status": "UP"}), 200
        else:
            return jsonify({"status": "DOWN"}), 503
    except Exception as e:
        return jsonify({"status": "DOWN", "error": str(e)}), 503

if __name__ == "__main__":
    app.run(debug=True)
