import os
from api_objects.api_utils import APIUtils

class UserProfileAPI(APIUtils):    

    def __init__(self, session):
        super().__init__(session)
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/user/profile'

    def send_request(self):        
        self.response = self.get_request()
        return self.response