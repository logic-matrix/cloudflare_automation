<h2 align="center"> Cloudflare Worker Analytics Automation </h2>

<p align="center"> This project is a **Cloudflare automation script** built with Python and Flask.  
It fetches analytics for **all Cloudflare Workers** over the past 24 hours using the Cloudflare GraphQL API.
</p>

## Features

- Automatically fetches analytics data such as:
  - Total requests
  - Subrequests
  - Errors
  - CPU time metrics (P50, P99)
  - Worker status and script names

- 📦 Saves all analytics data to a `workers_dat.json` file locally.

- 📧 If any Worker exceeds a defined resource threshold (e.g., requests > 1), the system **sends an email alert to the client**.


>  **Do not commit your `.env` file**. It contains sensitive credentials.

##  How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```
2. Start the Flask server:
```
python app.py
```

```
<h2 align="center"> Notes </h2>
- Change GraphQL API endpoint
- Change email credentials
- Change email send condition value 
```

### Cloudflaire Api Resource
https://developers.cloudflare.com/api/resources/workers/subresources/scripts/methods/delete/