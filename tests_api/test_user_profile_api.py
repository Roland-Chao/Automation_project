import allure, json
from api_objects.login_api import LoginAPI
from api_objects.user_profile_api import UserProfileAPI
from page_objects.database_utils import DatabaseUtils

class TestUserProfileAPI:

    def test_get_profile_succuess(self, session, login_info):
        login = LoginAPI(session)
        profile = UserProfileAPI(session)
        db = DatabaseUtils()
        
        login_payload = {
            "provider": "native",
            "email": login_info["account"],
            "password": login_info["password"]
        }
        
        with allure.step("Login and get token"):
            login.set_login_api_payload(login_payload)
            login_response = login.send_request()
            token = login_response.json()["data"]["access_token"]
            session.headers = {'Authorization': 'Bearer ' + token}
            
            assert login_response.status_code == 200, f'{login_response.status_code}'
            
        with allure.step("send request"):
            profile_response = profile.send_request()
            
        with allure.step("assert status_code = 200"):
            assert profile_response.status_code == 200, f'{profile_response.status_code}'
        
        with allure.step("select db data"):
            query_string = ("SELECT id, provider, name, email, picture \
                            FROM stylish_backend.user WHERE access_token=%s;")
            query_data = (token,)
            db.execute_query(query_string, query_data)

        with allure.step("assert response data = db data"):
            db_result = db.fetchone_result()
            result = profile_response.json()["data"]
            
            assert db_result["name"] == result["name"], f'{db_result["email"]}'
            assert db_result["email"] == result["email"], f'{db_result["email"]}'
            assert db_result["picture"] == result["picture"], f'{db_result["picture"]}'
            assert db_result["provider"] == result["provider"], f'{db_result["provider"]}'
 
    def test_get_profile_without_token(self, session):
        profile = UserProfileAPI(session)

        with allure.step(f"send request"):
            response = profile.send_request()
        
        with allure.step(f'assert status_code = 401'):
            assert response.status_code == 401 , f'{response.status_code}'
            
        with allure.step(f'assert errorMsg = Unauthorized'):
            err_msg = response.json()["errorMsg"]
            assert err_msg == "Unauthorized" , f'{err_msg}'