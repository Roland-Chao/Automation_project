import pytest, allure, json
from api_objects.product_api import ProductAPI
from page_objects.database_utils import DatabaseUtils

class TestProductAPI:
    
    category = ["women", "men", "accessories"]
    @pytest.mark.parametrize('test_data', category)
    def test_get_product_with_vaild_category(self, session, test_data):
        product = ProductAPI(session, test_data)
    
        with allure.step("send request"):
            response = product.send_request(0)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 200, f'{response.status_code}'

        with allure.step("assert response category = women"):
            data = response.json()["data"]
            for index in data:
                assert index["category"] == test_data, f'{index["category"]}'

    @pytest.mark.parametrize('test_data', category)
    def test_get_product_total(self, session, test_data):
        product = ProductAPI(session, test_data)
        db = DatabaseUtils()
        
        with allure.step(f"get total product"):
            # 取得每一頁商品數，算出total，比對DB數量是否正確
            # paging 太多時不建議這樣做..會頻繁打api
            paging = 0
            total = 0
            while True :
                response = product.send_request(paging)
                assert response.status_code == 200, f'{response.status_code}'
                if len(response.json()["data"]) == 0 :
                    break
                else:
                    paging += 1
                    total += len(response.json()["data"])
                
        with allure.step(f"select db data by category: {test_data}"):
            query_string = ("SELECT * FROM stylish_backend.product where category=%s;")
            query_data = (test_data,)
            db.execute_query(query_string, query_data)
            db_result = db.fetchall_result()
            db.commit_query()
        
        with allure.step("assert response total = db total"):
            assert total == len(db_result), f"{total}"
            
    def test_get_product_with_invaild_category(self, session):
        product = ProductAPI(session, "abcdefg")
    
        with allure.step("send request"):
            response = product.send_request(0)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 400, f'{response.status_code}'

        with allure.step("assert response category = women"):
            error_msg = response.json()["errorMsg"]
            
            assert error_msg == "Invalid Category", f'{error_msg}'

    def test_get_product_with_invaild_paging(self, session):
        product = ProductAPI(session, "women")
    
        with allure.step("send request"):
            response = product.send_request(-1)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 500, f'{response.status_code}'

        with allure.step("assert response category = women"):
            error_msg = response.json()["errorMsg"]
            assert error_msg == "Internal Server Error", f'{error_msg}'