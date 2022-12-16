import os
from api_objects.api_utils import APIUtils

class ProductDetailsAPI(APIUtils):    

    def __init__(self, session):
        super().__init__(session)
        self.session = session
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/products/details'

    def send_request(self, product_id):
        self.session.params = {"id": product_id}
        self.response = self.get_request()
        return self.response