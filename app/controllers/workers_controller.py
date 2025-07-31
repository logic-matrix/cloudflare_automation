from datetime import datetime, timedelta, timezone 
from flask import json, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Cloudflare API credentials from .env
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_GRAPHQL_ENDPOINT = "https://api.cloudflare.com/client/v4/graphql"


def get_worker_analytics():
    # Calculate last 24 hours UTC range
    datetime_end = datetime.now(timezone.utc)
    datetime_start = datetime_end - timedelta(days=1)

    # Format timestamps in ISO8601
    datetime_start_str = datetime_start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    datetime_end_str = datetime_end.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    graphql_query = """
    query GetAllWorkersAnalytics($accountTag: string, $datetimeStart: string, $datetimeEnd: string) {
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
        "datetimeStart": datetime_start_str,
        "datetimeEnd": datetime_end_str
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
        data = response.json()

        # Save to workers_dat.json
        with open("workers_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return jsonify(data)
    else:
        return jsonify({"error": response.text}), response.status_code