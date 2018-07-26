
import binascii
import hashlib
import hmac
import json
import uuid
import requests

class UnleashedApi:
    base_url = "https://api.unleashedsoftware.com/"

    def __init__(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key.encode('utf-8')

    def post(self, path, data):
        hashed_query = hmac.new(self.api_key, b'', hashlib.sha256)
        signature = binascii.b2a_base64(hashed_query.digest())[:-1]

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-auth-id': self.api_id,
            'api-auth-signature': signature,
        }

        print(headers)
        print("---")
        print(data)
        print("===")
        resp = requests.post(
            self.base_url + path,
            json.dumps(data),
            headers=headers
        )

        return resp

def create_sales_order(api):
    guid = str(uuid.uuid4())
    data = {
        "Guid": guid,
        "Customer": {
            "CustomerCode": "T0001",
        },
        "OrderNumber": "SO-INS-5000",
        "OrderStatus": "Parked",
        "Tax": {
            "TaxCode": "VAT-18",
        },
        "SalesOrderLines": [{
            "LineNumber": 1,
            "Product": {
                "ProductCode": "AMP-B060"
            },
            "UnitPrice": 690,
            "OrderQuantity": 2,
            "LineTotal": 690 * 2,
        }, {
            "LineType": "Charge",
            "Product": {
                "ProductDescription": "Курьерская доставка"
            },
            "OrderQuantity": 1,
            "UnitPrice": 250,
            "LineTotal": 250,
        }],
        "SubTotal": 690 * 2 + 250,
        "Total": 690 * 2 + 250
    }

    resp = api.post('/SalesOrders/' + guid, data)
    print('code', resp.status_code)
    print('---')
    from pprint import pprint
    pprint(resp.json())
