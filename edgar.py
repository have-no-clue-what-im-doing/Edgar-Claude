import requests
import json

api_key = '968318464bad1394b290cb06e6c380003517d0313a84c4ced3c20bd1eac8501d'


url = "https://api.sec-api.io"


headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
}

ticker = 'AAPL'
formType = '10-K'

data = {
    "query": f"ticker:{ticker} AND formType:{formType}",
    "from": "0",
    "size": "10",
    "sort": [{"filedAt": {"order": "desc"}}]
}


response = requests.post(url, headers=headers, data=json.dumps(data))


if response.status_code == 200:
    ten_k_list = response.json()
    ten_k_list_json = (json.dumps(ten_k_list, indent=4))
    ten_k_list_filings_list = ten_k_list['filings']
    #print(ten_k_list_filings_list)
    #print(ten_k_list_json)
    #print(ten_k_list['filings'][0]['linkToFilingDetails'])
    print(len(ten_k_list_filings_list))
    for listing in ten_k_list_filings_list:
        print(listing['linkToFilingDetails'])
    
else:
    print(f"Error: {response.status_code}, {response.text}")

def Get10K():
    pass