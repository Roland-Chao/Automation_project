import allure, pytest, os, json
from api_objects.login_api import LoginAPI
from page_objects.database_utils import DatabaseUtils
from test_data.get_data_from_excel import GetDataFromExcel

class TestLoginAPI:
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)
    
    def test_login_succuess(self, session, login_info):
        login = LoginAPI(session)
        db = DatabaseUtils()
        
        login_payload = {
            "provider": "native",
            "email": login_info["account"],
            "password": login_info["password"]
        }

        with allure.step("create login payload"):
            login.set_login_api_payload(login_payload)
            
        with allure.step("assert status_code and user info"):
            response = login.send_request()
            user_info = response.json()["data"]["user"]

            assert response.status_code == 200 , f'{response.status_code}'
            assert user_info["provider"] == login_payload["provider"]
            assert user_info["email"] == login_payload["email"]
            
        with allure.step("select db data"):
            query_string = ("SELECT access_token, access_expired, id, provider, name, email \
                            FROM stylish_backend.user where email=%s;")
            query_data = (login_info["account"],)
            
            db.execute_query(query_string, query_data)
            
        with allure.step(f'Verify the email colum value = {login_payload["email"]}'):
            db_result = db.fetchone_result()
            api_result = response.json()["data"]
            
            assert db_result["id"] == api_result["user"]["id"], f'{db_result["id"]}'
            assert db_result["name"] == api_result["user"]["name"], f'{db_result["name"]}'
            assert db_result["email"] == api_result["user"]["email"], f'{db_result["email"]}'
            assert db_result["provider"] == api_result["user"]["provider"], f'{db_result["provider"]}'
            assert db_result["access_token"] == api_result["access_token"], f'{db_result["access_token"]}'
            assert db_result["access_expired"] == int(api_result["access_expired"]), f'{db_result["access_expired"]}'
            
    @pytest.mark.parametrize('test_data', data.create_test_data("API Login invaild value"))
    def test_login_with_invaild_value(self, session, test_data):
        login = LoginAPI(session)

        with allure.step(f"create login payload: {test_data}"):
            login.set_login_api_payload(test_data)
        
        with allure.step(f'send request'):
            response = login.send_request()
        
        with allure.step(f'assert status_code = {test_data["status_code"]}'):
            assert response.status_code == int(test_data["status_code"]) , f'{response.status_code}'