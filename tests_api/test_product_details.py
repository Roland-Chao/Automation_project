import pytest, allure, json
from api_objects.product_details import ProductDetailsAPI

class TestProductDetailsAPI:
    
    @pytest.mark.parametrize('product_id', [201807202140, 201807242216, 201807201824])
    def test_product_details_with_correct_id(self, session, database, product_id):
        product_search = ProductDetailsAPI(session)
        
        with allure.step("send request"):
            response = product_search.send_request(product_id)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 200, f'{response.status_code}'
            
        with allure.step(f"assert response id = {product_id}"):
            response_data = response.json()["data"]
            assert response_data["id"] == product_id, f'{response_data["id"]}'
    
        with allure.step(f"select db data by id: {product_id}"):
            query_string = ("SELECT * FROM stylish_backend.product WHERE id=%s;")
            query_data = (product_id,)
            database.execute_query(query_string, query_data)
            db_result = database.fetchone_result()
            database.commit_query()
            
        with allure.step(f"assert db_data = response_data"):  
            assert db_result["id"] == response_data["id"], f'{db_result["id"]}'
            assert db_result["category"] == response_data["category"], f'{db_result["category"]}'
            assert db_result["title"] == response_data["title"], f'{db_result["title"]}'
            assert db_result["description"] == response_data["description"], f'{db_result["description"]}'
            assert db_result["price"] == response_data["price"], f'{db_result["price"]}'
            assert db_result["texture"] == response_data["texture"], f'{db_result["texture"]}'
            assert db_result["wash"] == response_data["wash"], f'{db_result["wash"]}'
            assert db_result["place"] == response_data["place"], f'{db_result["place"]}'
            assert db_result["note"] == response_data["note"], f'{db_result["note"]}'
            assert db_result["story"] == response_data["story"], f'{db_result["story"]}'

    def test_product_details_with_invaild_id(self, session):
        product_details = ProductDetailsAPI(session)
        product_id = 123
        
        with allure.step("send request"):
            response = product_details.send_request(product_id)
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 400, f'{response.status_code}'
            
        with allure.step(f"assert error_msg = Invalid Product ID"):
            error_msg = response.json()["errorMsg"]
            assert error_msg == "Invalid Product ID", f'{error_msg}'

    def test_product_details_with_invaild_category(self, session):
        # 這裡不知道為什麼，帶英文的id會噴 Invalid Category
        product_details = ProductDetailsAPI(session)
        product_id = "roland"
        
        with allure.step("send request"):
            response = product_details.send_request(product_id)
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 400, f'{response.status_code}'
            
        with allure.step(f"assert error_msg = Invalid Category"):
            error_msg = response.json()["errorMsg"]
            assert error_msg == "Invalid Category", f'{error_msg}'
            
    def test_product_details_with_empty_id(self, session):
        product_details = ProductDetailsAPI(session)
        product_id = None
        
        with allure.step("send request"):
            response = product_details.send_request(product_id)
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 400, f'{response.status_code}'
            
        with allure.step(f"assert error_msg = Invalid Category"):
            error_msg = response.json()["errorMsg"]
            assert error_msg == "Invalid Category", f'{error_msg}'