import os
from flask import Flask, render_template
import requests
from threading import Timer

app = Flask(__name__)

# Charger les URLs des services depuis les variables d'environnement
SERVICES = {
    "bdd": os.getenv("SERVICE_BDD", "http://example-bdd-service"),
    "grafana": os.getenv("SERVICE_GRAFANA", "http://example-grafana"),
    "meteo": os.getenv("SERVICE_METEO", "https://portail-api.meteofrance.fr/web/fr/"),
    "site": os.getenv("SERVICE_SITE", "http://example-site"),
}

# Statut initial des services
service_status = {key: False for key in SERVICES}

def check_services():
    global service_status
    for service, url in SERVICES.items():
        try:
            response = requests.head(url, timeout=5)
            service_status[service] = response.ok
        except requests.RequestException:
            service_status[service] = False
    Timer(30, check_services).start()  # Vérifier toutes les 30 secondes

@app.route("/")
def index():
    return render_template("index.html", statuses=service_status)

if __name__ == "__main__":
    check_services()  # Lancer la vérification en arrière-plan
    app.run(host="0.0.0.0", port=5000)
