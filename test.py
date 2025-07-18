import requests

url = "https://api.cloudflare.com/client/v4/accounts/fa92e8c102c73480191927c263d2d76/workers/scripts"
headers = {
    "Authorization": "PP5ngeYgeunKboVXEzAQ5UmwKjSvLlUGqwN_sr7t",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
