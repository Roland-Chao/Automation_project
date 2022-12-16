import pytest, allure, json
from api_objects.product_search import ProductSearchAPI

class TestProductSearchAPI:
    
    keyword = ["西裝", "洋裝", "衫"]
    @pytest.mark.parametrize('test_data', keyword)
    def test_product_search_with_vaild_keyword(self, session, database, test_data):
        product_search = ProductSearchAPI(session)
        
        with allure.step("send request"):
            response = product_search.send_request(test_data, 0)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 200, f'{response.status_code}'

        with allure.step("assert response category = women"):
            response_data = response.json()["data"]
            for index in range(len(response_data)):
                assert test_data in response_data[index]["title"], f'{response_data[index]["title"]}'
        
        with allure.step(f"select db data by category: "):
            query_string = ("SELECT * FROM stylish_backend.product WHERE title LIKE CONCAT('%', %s, '%');")
            query_data = (test_data,)
            database.execute_query(query_string, query_data)
            db_result = database.fetchall_result()
            database.commit_query()
        
        with allure.step("assert db data = response_data"):
            assert len(response_data) == len(db_result), f"{len(response_data)}"
            for index in range(len(db_result)):
                assert db_result[index]["title"] == response_data[index]["title"], f'{db_result[index]["title"]}'

    def test_get_product_with_invaild_keyword(self, session, database):
        product_search = ProductSearchAPI(session)
        keyword = "Roland"
        
        with allure.step("send request"):
            response = product_search.send_request(keyword, 0)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 200, f'{response.status_code}'

        with allure.step("assert response data = 0"):
            response_data = response.json()["data"]
            assert len(response_data) == 0, f'{response_data}'
        
        with allure.step(f"select db data by category: "):
            query_string = ("SELECT * FROM stylish_backend.product WHERE title LIKE CONCAT('%', %s, '%');")
            query_data = (keyword,)
            database.execute_query(query_string, query_data)
            db_result = database.fetchall_result()
            database.commit_query()
            
        with allure.step(f"assert db data = response_data"):
            assert len(db_result) == len(response_data), f'{db_result}'

    def test_get_product_with_empty_keyword(self, session):
        product_search = ProductSearchAPI(session)
        keyword = " "
        
        with allure.step("send request"):
            response = product_search.send_request(keyword, 0)
            
        with allure.step("assert status_code = 200"):
            assert response.status_code == 200, f'{response.status_code}'

        with allure.step("assert response data = 0"):
            response_data = response.json()["data"]
            assert len(response_data) == 0, f'{response_data}'
            
    def test_get_product_without_keyword(self, session):
        product_search = ProductSearchAPI(session)
        keyword = None
        
        with allure.step("send request"):
            response = product_search.send_request(keyword, 0)
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 400, f'{response.status_code}'

        with allure.step("assert errorMsg = Search Keyword is required"):
            response_data = response.json()["errorMsg"]
            assert response_data == "Search Keyword is required.", f'{response_data}'