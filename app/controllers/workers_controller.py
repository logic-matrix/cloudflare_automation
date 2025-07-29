from flask import  jsonify
import requests
from dotenv import load_dotenv

 

load_dotenv()
# Cloudflare API Credentials (replace these with environment variables in production)
CF_API_TOKEN = "HqBuAMJ5YuDcLWr5eoe5G3g7g70XYWhkTLlzR6sJ"
CF_ACCOUNT_ID = "9fa92e8c102c73480191927c263d2d76"
CF_GRAPHQL_ENDPOINT = "https://api.cloudflare.com/client/v4/graphql"


def get_worker_analytics(method='GET'):
    # Updated datetime range (1-day gap)
    datetime_start = "2025-07-22T00:00:00.000Z"
    datetime_end = "2025-07-25T23:59:59.000Z"
    script_name = "gentle-glade-6848"

    graphql_query = """
    query GetWorkersAnalytics($accountTag: string, $datetimeStart: string, $datetimeEnd: string, $scriptName: string) {
      viewer {
        accounts(filter: {accountTag: $accountTag}) {
          workersInvocationsAdaptive(limit: 100, filter: {
            scriptName: $scriptName,
            datetime_geq: $datetimeStart,
            datetime_leq: $datetimeEnd
          }) {
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
        "datetimeEnd": datetime_end,
        "scriptName": script_name
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

