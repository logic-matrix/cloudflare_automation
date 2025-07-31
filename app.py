from flask import Flask, json, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
