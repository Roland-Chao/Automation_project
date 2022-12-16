import os
from api_objects.api_utils import APIUtils

class ProductSearchAPI(APIUtils):    

    def __init__(self, session):
        super().__init__(session)
        self.session = session
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/products/search'

    def send_request(self, keyword, paging):
        self.session.params = {"keyword": keyword,
                               "paging": paging}
        self.response = self.get_request()
        return self.response