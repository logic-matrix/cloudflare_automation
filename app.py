from flask_mail import Mail,Message
from flask import Flask, current_app, json, render_template, jsonify
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

 ###########################################################################################
 ###########################################################################################
@app.route('/')
def worker_table():
    with open('workers_summary.json') as f:
        data = json.load(f)

    workers_summary = data["workers_summary"]
    total_summary = data["total_summary"]

    return render_template('index.html', workers=workers_summary, total=total_summary)


########################################################################################
########################################################################################
@app.route('/worker-analytics', methods=['GET'])
def worker_analytics_route():
    get_worker_analytics()
    #summarize_workers()
    email()  # Call email function to send alerts if needed
    return  jsonify({"message": "Worker analytics processed and email sent if needed."})


#########################################################################################
#########################################################################################
@app.route('/email', methods=['get'])
def email():
    try:
        # Load worker data
        with open("workers_summary.json") as f:
            data = json.load(f)

        workers = data.get("workers_summary", {})

        # Find workers with requests > 100
        over_limit = []
        for name, stats in workers.items():
            if stats.get("total_requests", 0) > 100:
                over_limit.append(f"{name} has {stats['total_requests']} requests")

        if over_limit:
            body = "The following workers are getting more than 100 requests per day:\n\n"
            body += "\n".join(over_limit)

            body  += "\n\n View Full Report: http://your-domain.com/static/report.html"
            msg = Message(
                subject='Cloudflare Worker Analytics Report',
                sender='tarikulabir69@gmail.com',
                recipients=['tarikulabir931@gmail.com']
            )
            msg.body = body

            with current_app.app_context():  # Ensure app context if called outside route
                mail.send(msg)
                print("📨 Email sent.")

            return "Email Sent"
        else:
            print("No workers exceeded request threshold.")
            return "No alerts to send"

    except Exception as e:
        print("Error in sending email:", str(e))
        return f"Error: {e}"

##########################################################################################
##########################################################################################
     
if __name__ == '__main__':
    app.run(debug=True)
