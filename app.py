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

# Replace with your real GitHub username and repo name
GITHUB_RAW_URL = "https://raw.githubusercontent.com/PearlGuide/squad-whitelist/main/RemoteAdminListHosts.cfg"

# Cache for fallback if GitHub is unavailable
cached_config = None

@app.route('/RemoteAdminListHosts.cfg')
def serve_cfg():
    global cached_config
    try:
        # Log access
        logging.info("PSG requested RemoteAdminListHosts.cfg")

        # Fetch latest content from GitHub
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            cached_config = response.text
            return Response(response.text, mimetype='text/plain')
        else:
            logging.warning(f"GitHub fetch failed: {response.status_code}")
            if cached_config:
                return Response(cached_config, mimetype='text/plain')
            return Response("Failed to fetch config from GitHub", status=500)

    except Exception as e:
        logging.error(f"Error serving .cfg file: {str(e)}")
        if cached_config:
            return Response(cached_config, mimetype='text/plain')
        return Response("Internal Server Error", status=500)

@app.route('/')
def index():
    return "Whitelist Server is Running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
