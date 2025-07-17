from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from cloudflare import Cloudflare

# Load environment variables
load_dotenv()

# Initialize Cloudflare and Flask
cf = Cloudflare(token=os.getenv("CF_API_TOKEN"))
account_id = os.getenv("CF_ACCOUNT_ID")
app = Flask(__name__)

# Route: Get list of Cloudflare Workers
@app.route('/workers', methods=['GET'])
def get_workers_list():
    try:
        scripts = cf.accounts.workers.scripts.get(account_id)
        worker_names = [script['id'] for script in scripts]
        return jsonify({"workers": worker_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Get analytics for a specific worker
@app.route('/workers/<string:script_name>/analytics', methods=['GET'])
def get_worker_analytics(script_name):
    try:
        analytics = cf.accounts.workers.scripts.analytics.get(
            account_id,
            script_name,
            params={
                'metrics': 'cpu_time,requests,subrequests,failures,status_4xx,status_5xx',
                'limit': 7,  # past 7 days
                'aggregate': 'sum',
                'dimensions': 'date'
            }
        )
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
