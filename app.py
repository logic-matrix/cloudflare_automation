from flask import Flask, json, render_template, jsonify
import requests

from app.controllers.email_controller import send_email
from app.controllers.workers_controller import get_worker_analytics 
  

app = Flask(__name__)

@app.route('/')
def worker_table():
    with open('workers_data.json') as f:
        data = json.load(f)

    rows = data["data"]["viewer"]["accounts"][0]["workersInvocationsAdaptive"]
    return render_template('index.html', rows=rows)



@app.route('/cloudflare/worker-analytics', methods=['GET'])
def worker_analytics_route():
    return get_worker_analytics()

@app.route('/email', methods=['get'])
def email_route():
    #result = send_email()
    if requests.status_code == 200:
        send_email()
        return jsonify({"message": "Email sent successfully"}), 200
    else: 
        return jsonify({"message":"Failed to send email"}), 500


if __name__ == '__main__':
    app.run(debug=True)
