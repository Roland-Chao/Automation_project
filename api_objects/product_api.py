import os
from api_objects.api_utils import APIUtils

class ProductAPI(APIUtils):    

    def __init__(self, session, category):
        super().__init__(session)
        self.session = session
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/products/{category}'

    def send_request(self, paging):
        self.session.params = {"paging": paging}
        self.response = self.get_request()
        return self.response