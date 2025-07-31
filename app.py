from flask import Flask

from app.controllers.workers_controller import get_worker_analytics_controller
  

app = Flask(__name__)

@app.route('/cloudflare/worker-analytics', methods=['GET'])
def worker_analytics_route():
    return get_worker_analytics_controller()

if __name__ == '__main__':
    app.run(debug=True)
