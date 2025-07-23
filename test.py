import requests

url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
headers = {
    "Authorization": "TIEv-cAGi5xD-fupYfvUWzinO_T0IqcSTM4QfeP9",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
