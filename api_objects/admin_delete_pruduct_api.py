import os
from api_objects.api_utils import APIUtils

class DeleteAdminProductAPI(APIUtils):  

    def __init__(self, session, product_id):
        super().__init__(session)
        self.session = session
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/admin/product/{product_id}'
        
    def send_request(self):
        self.response = self.delete_request()
        return self.response