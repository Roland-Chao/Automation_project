import os, json
from api_objects.api_utils import APIUtils

class GetOrderAPI(APIUtils):    

    def __init__(self, session, order_number):
        super().__init__(session)
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/order/{order_number}'

    def send_request(self):
        return self.get_request()