import requests

url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
headers = {
    "Authorization": "TIEv-cAGi5xD-fupYfvUWzinO_T0IqcSTM4QfeP9",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
########################################################################
########## Previous version##############
from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Cloudflare API Credentials (replace these with environment variables in production)
CF_API_TOKEN = "HqBuAMJ5YuDcLWr5eoe5G3g7g70XYWhkTLlzR6sJ"
CF_ACCOUNT_ID = "9fa92e8c102c73480191927c263d2d76"
CF_GRAPHQL_ENDPOINT = "https://api.cloudflare.com/client/v4/graphql"

@app.route('/cloudflare/worker-analytics', methods=['GET'])
def get_worker_analytics():
    datetime_start = "2025-07-22T00:00:00.000Z"
    datetime_end = "2025-07-25T23:59:59.000Z"

    graphql_query = """
    query GetWorkersAnalytics($accountTag: string, $datetimeStart: string, $datetimeEnd: string) {
      viewer {
        accounts(filter: {accountTag: $accountTag}) {
          workersInvocationsAdaptive(
            limit: 100,
            filter: {
              datetime_geq: $datetimeStart,
              datetime_leq: $datetimeEnd
            }
          ) {
            sum {
              subrequests
              requests
              errors
            }
            quantiles {
              cpuTimeP50
              cpuTimeP99
            }
            dimensions {
              datetime
              scriptName
              status
            }
          }
        }
      }
    }
    """

    variables = {
        "accountTag": CF_ACCOUNT_ID,
        "datetimeStart": datetime_start,
        "datetimeEnd": datetime_end
    }

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "query": graphql_query,
        "variables": variables
    }

    response = requests.post(CF_GRAPHQL_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)


#############################################################################
from flask_mail import Mail,Message
from flask import Flask, json, render_template, jsonify
import requests
from app.controllers.email_controller import send_email
from app.controllers.workers_controller import get_worker_analytics 
  

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
    with open('workers_data.json') as f:
        data = json.load(f)

    rows = data["data"]["viewer"]["accounts"][0]["workersInvocationsAdaptive"]
    return render_template('index.html', rows=rows)



@app.route('/cloudflare/worker-analytics', methods=['GET'])
def worker_analytics_route():
    return get_worker_analytics()

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
