from collections import defaultdict
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
    datetime_start_str = "2025-07-22T00:00:00.000Z"
    datetime_end_str = "2025-07-25T23:59:59.000Z"

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




##############################################################################################################################

def summarize_workers():
    try:
        # Load raw data
        with open("workers_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        workers_data = data["data"]["viewer"]["accounts"][0]["workersInvocationsAdaptive"]
        summary = defaultdict(lambda: {
            "total_requests": 0,
            "total_subrequests": 0,
            "total_errors": 0,
            "cpuTimeP50_sum": 0.0,
            "cpuTimeP99_sum": 0.0,
            "entries": 0
        })

        for entry in workers_data:
            dims = entry["dimensions"]
            script_name = dims["scriptName"]

            summary[script_name]["total_requests"] += entry["sum"]["requests"]
            summary[script_name]["total_subrequests"] += entry["sum"]["subrequests"]
            summary[script_name]["total_errors"] += entry["sum"]["errors"]
            summary[script_name]["cpuTimeP50_sum"] += entry["quantiles"]["cpuTimeP50"]
            summary[script_name]["cpuTimeP99_sum"] += entry["quantiles"]["cpuTimeP99"]
            summary[script_name]["entries"] += 1

        # Final summary list
        result = {}
        grand_total = {
            "total_requests": 0,
            "total_subrequests": 0,
            "total_errors": 0,
            "cpuTimeP50_avg": 0.0,
            "cpuTimeP99_avg": 0.0,
        }

        for script, stats in summary.items():
            cpuTimeP50_avg = stats["cpuTimeP50_sum"] / stats["entries"]
            cpuTimeP99_avg = stats["cpuTimeP99_sum"] / stats["entries"]

            result[script] = {
                "total_requests": stats["total_requests"],
                "total_subrequests": stats["total_subrequests"],
                "total_errors": stats["total_errors"],
                "cpuTimeP50_avg": round(cpuTimeP50_avg, 2),
                "cpuTimeP99_avg": round(cpuTimeP99_avg, 2)
            }

            # Accumulate into grand total
            grand_total["total_requests"] += stats["total_requests"]
            grand_total["total_subrequests"] += stats["total_subrequests"]
            grand_total["total_errors"] += stats["total_errors"]
            grand_total["cpuTimeP50_avg"] += cpuTimeP50_avg
            grand_total["cpuTimeP99_avg"] += cpuTimeP99_avg

        # Average CPU times across workers
        total_workers = len(summary)
        grand_total["cpuTimeP50_avg"] = round(grand_total["cpuTimeP50_avg"] / total_workers, 2)
        grand_total["cpuTimeP99_avg"] = round(grand_total["cpuTimeP99_avg"] / total_workers, 2)

        final_output = {
            "workers_summary": result,
            "total_summary": grand_total
        }
         

        # Save to summary JSON
        with open("workers_summary.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2)
        return jsonify(final_output)

        #print("Summary generated and saved to workers_summary.json")

    except Exception as e:
        print(f"Error: {e}")

 
