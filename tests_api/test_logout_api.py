import allure, os, json
from api_objects.login_api import LoginAPI
from api_objects.logout_api import LogoutAPI
from page_objects.database_utils import DatabaseUtils
from test_data.get_data_from_excel import GetDataFromExcel

class TestLogoutAPI:
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)

    def test_logout_succuess(self, session, login_info):
        login = LoginAPI(session)
        logout = LogoutAPI(session)
        db = DatabaseUtils()
        login_payload = {
            "provider": "native",
            "email": login_info["account"],
            "password": login_info["password"]
        }
        with allure.step("login and get login token"):
            login.set_login_api_payload(login_payload)
            login_res = login.send_request()
            token = login_res.json()["data"]["access_token"]
            session.headers = {'Authorization': 'Bearer ' + token}
            
            assert login_res.status_code == 200 , f'{login_res.status_code}'

        with allure.step("query db"):
            query_string = ("SELECT access_token FROM stylish_backend.user WHERE email=%s;")
            query_data = (login_info["account"],)
            db.execute_query(query_string, query_data)
            db_login_result = db.fetchone_result()
            db.commit_query()

        with allure.step(f'Verify the email colum value = {login_payload["email"]}'):
            assert db_login_result["access_token"] == token, f'{db_login_result["access_token"]}'
            
        with allure.step("send logout request"):
            logout_res = logout.send_request()
        
        with allure.step("assert status_code = 200 \
                        assert message = Logout Success"):
            assert logout_res.status_code == 200 , f'{logout_res.status_code}'
         
        with allure.step("assert message = Logout Success"):
            msg = logout_res.json()["message"]
            assert msg == "Logout Success" , f'{msg}'

        with allure.step("select access_token by email"):
            query_string2 = ("SELECT access_token FROM stylish_backend.user WHERE email=%s;")
            query_data2 = (login_info["account"],)
            db.execute_query(query_string2, query_data2)
            db_result2 = db.fetchone_result()

        with allure.step("assert access_token = None "):
            assert db_result2["access_token"] == '', f'{db_result2}'
            
    def test_logout_without_token(self, session):
        logout = LogoutAPI(session)

        with allure.step("set request"):
            logout_res = logout.send_request()
        
        with allure.step("assert status_code = 401"):
            assert logout_res.status_code == 401 , f'{logout_res.status_code}'
            
        with allure.step("assert message = Unauthorized"):
            msg = logout_res.json()["errorMsg"]
            assert msg == "Unauthorized" , f'{msg}'
    
    def test_logout_use_token_twice(self, session, login_info):
        login = LoginAPI(session)
        logout = LogoutAPI(session)
        login_payload = {
            "provider": "native",
            "email": login_info["account"],
            "password": login_info["password"]
        }
        
        with allure.step("login and get login token"):
            login.set_login_api_payload(login_payload)
            login_res = login.send_request()
            token = login_res.json()["data"]["access_token"]
            session.headers = {'Authorization': 'Bearer ' + token}
            
            assert login_res.status_code == 200 , f'{login_res.status_code}'
            
        with allure.step("send logout request"):
            logout_res = logout.send_request()
        
        with allure.step("assert status_code = 200"):
            assert logout_res.status_code == 200 , f'{logout_res.status_code}'
        
        with allure.step("assert message = Logout Success"):
            msg = logout_res.json()["message"]
            assert msg == "Logout Success" , f'{msg}'

        with allure.step("send logout again"):
            logout_res_2 = logout.send_request()

        with allure.step("assert status_code = 403"):
            assert logout_res_2.status_code == 403, f'{logout_res_2.status_code}'
        
        with allure.step("assert errorMsg = Invalid Access Token"):
            msg_2 = logout_res_2.json()["errorMsg"]
            assert msg_2 == "Invalid Access Token" , f'{msg_2}'

    def test_logout_use_invaild_token(self, session):
        logout = LogoutAPI(session)
            
        with allure.step("set invaild token and send logout request"):
            session.headers = {'Authorization': '12345'}
            logout_res = logout.send_request()
        
        with allure.step("assert status_code = 403"):
            assert logout_res.status_code == 403 , f'{logout_res.status_code}'
        
        with allure.step("assert message = Logout Success"):
            msg = logout_res.json()["errorMsg"]
            assert msg == "Forbidden" , f'{msg}'