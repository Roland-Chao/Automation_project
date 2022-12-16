import os
from api_objects.api_utils import APIUtils

class LoginAPI(APIUtils):    
    
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/user/login'

    def set_login_api_payload(self, data):
        self.body = data
    
    def send_request(self):        
        return self.post_request(json=self.body)
    
    def set_login_token_to_session(self, login_info):
        login_payload = {
            "provider": "native",
            "email": login_info["account"],
            "password": login_info["password"]
        }
        self.set_login_api_payload(login_payload)
        token = self.send_request().json()["data"]["access_token"]
        self.session.headers = {'Authorization': 'Bearer ' + token}