import pytest, allure, json, os
from api_objects.login_api import LoginAPI
from page_objects.prime_page import PrimePage
from api_objects.order_api import OrderAPI
from page_objects.database_utils import DatabaseUtils
from test_data.get_data_from_excel import GetDataFromExcel

class TestOrderAPI:
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)
    order_data = {
        "prime": "",
        "order": {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": 799,
            "freight": 30,
            "total": 829,
            "recipient": {
                "name": "dddd",
                "phone": "0988065185",
                "email": "kenny66306@hotmail.com",
                "address": "Address",
                "time": "morning"
            },
            "list": [
                {
                    "color": {
                    "code": "FFFFFF",
                    "name": "白色"
                    },
                    "id": 201807201824,
                    "image": "http://54.201.140.239/assets/201807201824/main.jpg",
                    "name": "前開衩扭結洋裝",
                    "price": 799,
                    "qty": 1,
                    "size": "S",
                    "stock": 9
                }
            ]
        }
    }
    def test_create_order_success(self, session, browser, login_info):
        login = LoginAPI(session)
        prime_page = PrimePage(browser)
        order = OrderAPI(session)
        db = DatabaseUtils()

        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("get prime key"):
            prime_key = prime_page.get_prime_key()
            request_data = self.order_data.copy()
            request_data["prime"] = prime_key
            
        with allure.step("set prime key and send order request"):
            order.set_order_api_payload(request_data)
            response = order.send_request()
            order_number = response.json()["data"]["number"]
            
            assert response.status_code == 200, f'{response.status_code}'
            assert order_number is not None, f'{order_number}'

        with allure.step(f"select db data by number: {order_number}"):
            query_string = ("SELECT * FROM stylish_backend.order_table WHERE number=%s;")
            query_data = (order_number,)
            db.execute_query(query_string, query_data)
            db_result = db.fetchone_result()
            db.commit_query()
        
        with allure.step("assert db data = request payload"):
            db_order_data = json.loads(db_result["details"])
            assert db_order_data == self.order_data["order"], f"{db_order_data}"
            assert db_result["total"] == self.order_data["order"]["total"], f'{db_result["total"]}'

    def test_create_order_without_token(self, session, browser):
            prime_page = PrimePage(browser)
            order = OrderAPI(session)
                
            with allure.step("get prime key"):
                prime_key = prime_page.get_prime_key()
                request_data = self.order_data.copy()
                request_data["prime"] = prime_key
                
            with allure.step("set prime key and send order request"):
                order.set_order_api_payload(request_data)
                response = order.send_request()
            
            with allure.step("assert status_code = 401"):
                error_msg = response.json()["errorMsg"]
                assert response.status_code == 401, f'{response.status_code}'  
                assert error_msg == "Unauthorized", f'{error_msg}'

    def test_create_order_without_prime(self, session, login_info):
        login = LoginAPI(session)
        order = OrderAPI(session)

        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)

        with allure.step("send order request"):
            order.set_order_api_payload(self.order_data.copy())
            response = order.send_request()

        with allure.step("assert status_code = 400"):
            assert response.status_code == 400, f'{response.status_code}'
            
        with allure.step("assert error_msg = Prime value is required."): 
            error_msg = response.json()["errorMsg"]
            assert error_msg == "Prime value is required.", f'{error_msg}'
            
    @pytest.mark.parametrize('test_data', data.create_test_data("API Order invaild value"))
    def test_create_order_with_invaild_value(self, session, browser, login_info, test_data):
        login = LoginAPI(session)
        prime_page = PrimePage(browser)
        order = OrderAPI(session)

        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("get prime key"):
            prime_key = prime_page.get_prime_key()
            
        with allure.step("send order request"):            
            test_data["prime"] = prime_key
            order.create_order_payload(test_data)
            response = order.send_request()
            
        with allure.step("assert status_code = 400"): 
            assert response.status_code == 400, f'{response.status_code}'
            
        with allure.step(f'assert error_msg = {test_data["message"]}'): 
            error_msg = response.json()["errorMsg"]
            assert error_msg == test_data["message"], f'{error_msg}'