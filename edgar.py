import requests
import json
from PyPDF2 import PdfReader, PdfWriter

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
        ten_k_list_filings_list = ten_k_list['filings']
        if ten_k_list_filings_list:
            return ten_k_list_filings_list[0]['linkToFilingDetails']
    print("No filings found or failed request.")
    return None


# Fetch the 10-K PDF URL
ten_k_pdf = Get10K(api_key, ticker, form_type, 0, 1)

if ten_k_pdf:
    url = f'https://api.sec-api.io/filing-reader?token={api_key}&url={ten_k_pdf}'
    response = requests.get(url)
    if response.status_code == 200:
        pdf_filename = f'{ticker}_10K.pdf'
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f'PDF downloaded as {pdf_filename}')
        #SPLIT PDF THING    
        reader = PdfReader(pdf_filename)
        total_pages = len(reader.pages)
        max_pages = 50

        for i in range(0, total_pages, max_pages):
            writer = PdfWriter()
            for j in range(i, min(i + max_pages, total_pages)):
                writer.add_page(reader.pages[j])
            
            split_filename = f'{ticker}_10K_part_{i // max_pages + 1}.pdf'
            with open(split_filename, 'wb') as split_file:
                writer.write(split_file)
            print(f'Created: {split_filename}')
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
else:
    print("Could not retrieve 10-K filing URL.")
