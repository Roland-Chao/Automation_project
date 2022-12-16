import pytest, allure, json, os
from api_objects.login_api import LoginAPI
from page_objects.prime_page import PrimePage
from api_objects.order_api import OrderAPI
from test_data.get_data_from_excel import GetDataFromExcel
from api_objects.get_order import GetOrderAPI

class TestGetOrderAPI:
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
    def test_get_order_success(self, session, browser, login_info):
        login = LoginAPI(session)
        prime_page = PrimePage(browser)
        order = OrderAPI(session)
        
        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("get prime key"):
            prime_key = prime_page.get_prime_key()
            request_data = self.order_data.copy()
            request_data["prime"] = prime_key
            
        with allure.step("create_order_number"):
            order.set_order_api_payload(request_data)
            order_res = order.send_request()
            order_number = order_res.json()["data"]["number"]
            assert order_res.status_code == 200, f'{order_res.status_code}'
            assert order_number is not None, f'{order_number}'
        
        with allure.step("assert status_code = 200"):
            get_order = GetOrderAPI(session, order_number)
            
            get_order_res = get_order.send_request()
            assert get_order_res.status_code == 200, f'{get_order_res.status_code}'

        with allure.step("assert response data = order_data"):
            get_order_data = get_order_res.json()["data"]["details"]
            assert get_order_data == self.order_data["order"], f'{get_order_data}'

    def test_get_order_with_invaild_order_number(self, session, login_info):
            login = LoginAPI(session)
            get_order = GetOrderAPI(session, "123456")

            with allure.step("get login token"):
                login.set_login_token_to_session(login_info)
                
            with allure.step("send request"):
                response = get_order.send_request()
            
            with allure.step("assert status_code = 400"):
                error_msg = response.json()["errorMsg"]
                assert response.status_code == 400, f'{response.status_code}'
                
            with allure.step("assert error_msg  = Order Not Found."):
                assert error_msg == "Order Not Found.", f'{error_msg}'

    def test_get_order_without_token(self, session):
            get_order = GetOrderAPI(session, "123456")
                
            with allure.step("send request"):
                response = get_order.send_request()
            
            with allure.step("assert status_code = 401"):
                error_msg = response.json()["errorMsg"]
                assert response.status_code == 401, f'{response.status_code}'
                
            with allure.step("assert error_msg  = Unauthorized"):
                assert error_msg == "Unauthorized", f'{error_msg}'

    def test_get_order_without_order_number(self, session, login_info):
            login = LoginAPI(session)
            get_order = GetOrderAPI(session, "123456")

            with allure.step("get login token"):
                login.set_login_token_to_session(login_info)
                
            with allure.step("send request"):
                response = get_order.send_request()
            
            with allure.step("assert status_code = 400"):
                assert response.status_code == 400, f'{response.status_code}'