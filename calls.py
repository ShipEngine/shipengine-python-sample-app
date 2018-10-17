import requests, json


def get_carriers(key):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/carriers"
    request = requests.get(url, headers=headers)

    if request.text == "Unauthorized":
        return (request.status_code,)
    else:
        return (request.status_code, request.json())

def add_fedex_account(key, payload):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/connections/carriers/fedex"
    request = requests.post(url, headers=headers, data=json.JSONEncoder().encode(payload))
    return (request.status_code, request.json())

def delete_fedex_account(key, accountNumber):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/connections/carriers/fedex/{}".format(accountNumber)
    request = requests.delete(url, headers=headers)
    return request.status_code

def create_shipment(key, shipmentData):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/shipments"
    request = requests.post(url, headers=headers, data=json.JSONEncoder().encode(shipmentData))
    return (request.status_code, request.json())

def get_rates_call(key, shipmentId, carrierId):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/rates"
    payload = {"shipment_id": shipmentId, "rate_options": {"carrier_ids": [carrierId]}}
    request = requests.post(url, headers=headers, data=json.JSONEncoder().encode(payload))
    return (request.status_code, request.json())

def create_label_from_rate(key, rateId, testLabel):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/labels/rates/{}".format(rateId)
    payload = {"test_label": testLabel, "label_format": "pdf"}
    request = requests.post(url, headers=headers, data=json.JSONEncoder().encode(payload))
    return (request.status_code, request.json())

def void_label_call(key, labelId):
    headers = {"api-key": key, "Content-type": "application/json"}
    url = "https://api.shipengine.com/v1/labels/{}/void".format(labelId)
    request = requests.put(url, headers=headers)

    try:
        return (request.status_code, request.json())
    except ValueError:
        return (request.status_code,)