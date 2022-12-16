import os
from api_objects.api_utils import APIUtils

class LogoutAPI(APIUtils):    

    def __init__(self, session):
        super().__init__(session)
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/user/logout'

    def send_request(self):        
        self.response = self.post_request()
        return self.response