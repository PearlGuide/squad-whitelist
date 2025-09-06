from flask import Flask, Response
import requests
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Enable logging to file
logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

GITHUB_RAW_URL = "https://raw.githubusercontent.com/<PearlGuide>/<squad=whitelist>/main/RemoteAdminListHosts.cfg"

@app.route('/RemoteAdminListHosts.cfg')
def serve_cfg():
    try:
        # Log access
        logging.info("PSG requested RemoteAdminListHosts.cfg")

        # Fetch latest content from GitHub
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code != 200:
            return Response("Failed to fetch config from GitHub", status=500)

        # Return config content
        return Response(response.text, mimetype='text/plain')
    
    except Exception as e:
        logging.error(f"Error serving .cfg file: {str(e)}")
        return Response("Internal Server Error", status=500)

@app.route('/')
def index():
    return "Whitelist Server is Running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
