from flask_mail import Mail,Message
from flask import Flask, json, render_template, jsonify
import requests
from app.controllers.workers_controller import get_worker_analytics, summarize_workers 
  

app = Flask(__name__)
mail = Mail(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tarikulabir69@gmail.com'
app.config['MAIL_PASSWORD'] = 'nytxrkgtiekibmej'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

 
@app.route('/')
def worker_table():
    with open('workers_summary.json') as f:
        data = json.load(f)

    workers_summary = data["workers_summary"]
    total_summary = data["total_summary"]

    return render_template('index.html', workers=workers_summary, total=total_summary)



@app.route('/worker-analytics', methods=['GET'])
def worker_analytics_route():
    get_worker_analytics()
    return  summarize_workers()

@app.route('/email', methods=['get'])
def index():
   msg = Message(
                'Cloudflare Worker Analytics Report',
                sender ='tarikulabir69@gmail.com',
                recipients = ['tarikulabir931@gmail.com']
               )
   msg.body = 'Hello World Workers are getting more than 1000 requests per day'
   mail.send(msg)
   return 'Sent'
     
     
if __name__ == '__main__':
    app.run(debug=True)
