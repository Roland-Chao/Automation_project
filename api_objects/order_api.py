import os, json
from api_objects.api_utils import APIUtils

class OrderAPI(APIUtils):    
    _payload = {
        "prime": "",
        "order": {
            "shipping": "",
            "payment": "",
            "subtotal": "",
            "freight": 0,
            "total": 0,
            "recipient": {
                "name": "",
                "phone": "",
                "email": "",
                "address": "",
                "time": ""
            },
            "list": []
        }
    }
    
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/order'
        
    def set_order_api_payload(self, data):
        self.body = data
    
    def create_order_payload(self ,data):
        self.body = self._payload.copy()
        self.body["prime"] = data["prime"]
        self.body["order"]["shipping"] = data["shipping"]
        self.body["order"]["payment"] = data["payment"]
        self.body["order"]["subtotal"] = int(data["subtotal"])
        self.body["order"]["freight"] = int(data["freight"])
        self.body["order"]["total"] = int(data["total"])
        self.body["order"]["list"] = [(json.loads(data["item"]))]
        self.body["order"]["recipient"]["name"] = data["name"]
        self.body["order"]["recipient"]["phone"] = data["phone"]
        self.body["order"]["recipient"]["email"] = data["email"]
        self.body["order"]["recipient"]["address"] = data["address"]
        self.body["order"]["recipient"]["time"] = data["time"]

    def send_request(self):        
        return self.post_request(json=self.body)