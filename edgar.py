import requests
import json

api_key = '968318464bad1394b290cb06e6c380003517d0313a84c4ced3c20bd1eac8501d'







ticker = 'AMD'
form_type = '10-K'


def Get10K(api_key, ticker, form_type, start, size):
    url = "https://api.sec-api.io"
    headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
    }
    data = {
    "query": f"ticker:{ticker} AND formType:\"{form_type}\"",
    "from": start,
    "size": size,
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
        #print(len(ten_k_list_filings_list))
        for listing in ten_k_list_filings_list:
            print(listing['linkToFilingDetails'])
            return(listing['linkToFilingDetails'])


ten_k_pdf = Get10K(api_key, ticker, form_type, 0, 1)

url =  f'https://api.sec-api.io/filing-reader?token={api_key}&url={ten_k_pdf}'

response = requests.get(url)
if response.status_code == 200:
    with open(f'{ticker}_10K.pdf', 'wb') as pdf_file:
        pdf_file.write(response.content)
        print('pdf file downloaded')
