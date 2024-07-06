import requests
import json
from rest_framework.response import Response
from rest_framework import status


def KhaltiInitiate(amount):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/api/khalti/verify",
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        
    })
    headers = {
        'Authorization': 'Key ef11cb7ef3f347f18560b8264248bd2b',
        'Content-Type': 'application/json',
    }

    response = requests.post( url, headers=headers, data=payload)
    print(response)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from Khalti"}
    else:
        return {"error": "Khalti initiation failed", "status_code": response.status_code, "response": response.text}
    

def KhaltiVerify(pidx):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"

    payload = json.dumps({
        "pidx": pidx
    })
    headers = {
        'Authorization': 'Key ef11cb7ef3f347f18560b8264248bd2b',
        'Content-Type': 'application/json',
    }

    response = requests.post( url, headers=headers, data=payload)
    print(response)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from Khalti"}
    else:
        return {"error": "Khalti verification failed", "status_code": response.status_code, "response": response.text}