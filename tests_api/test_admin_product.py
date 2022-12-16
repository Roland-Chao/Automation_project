import pytest, allure, json, os, requests
from api_objects.login_api import LoginAPI
from page_objects.database_utils import DatabaseUtils
from api_objects.admin_pruduct_api import AdminProductAPI
from test_data.get_data_from_excel import GetDataFromExcel
from api_objects.admin_delete_pruduct_api import DeleteAdminProductAPI

class TestAdminProductAPI:
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)
    _files = {
        'main_image': open('test_data/otherImage0.jpg', 'rb'),
        'other_images': open('test_data/otherImage0.jpg', 'rb'),
        'other_images': open('test_data/otherImage0.jpg', 'rb')
    }
    _payload =  {
        'category': 'women', 
        'title': 'Roland_測試新增商品', 
        'description': '詳細內容', 
        'price': '100', 
        'texture': '棉', 
        'wash': '手洗', 
        'place': 'Taiwan', 
        'note': 'Notes', 
        'color_ids': '2', 
        'sizes': 'S', 
        'story': 'Story Content'
    }
        
    @pytest.mark.parametrize('test_data', data.create_test_data("API Create Product Failed"))
    def test_Admin_product_with_invaild_value(self, session, login_info, test_data):
        login = LoginAPI(session)
        Admin_product = AdminProductAPI(session)

        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("create request payload"):
            from_data = Admin_product.set_from_data(test_data)
            from_file = Admin_product.set_from_file(test_data)
        
        try:
            with allure.step("send Admin product request"):
                response = Admin_product.send_request(data=from_data, files=from_file)
                
            with allure.step("assert status_code = 400"):
                assert response.status_code == 400, f'{response.status_code}'
            
            with allure.step(f'assert errorMsg = {test_data["Error Msg"]}'):
                assert response.json()["errorMsg"] == test_data["Error Msg"], f'{from_data}'
                
        except AssertionError:
            with allure.step(f'delete prduct'):
                if response.status_code == 200:
                    product_id = response.json()["data"]["product_id"]
                    delete_product = DeleteAdminProductAPI(session, product_id)
                    delete = delete_product.send_request()
                    assert delete.status_code == 200, f"{delete.status_code}"
                    
            with allure.step(f'no product can delete'):     
                raise AssertionError(f"assert error: {response.json()}")
        
    def test_Admin_product_with_vaild_value(self, session, login_info):
        login = LoginAPI(session)
        Admin_product = AdminProductAPI(session)
        db = DatabaseUtils()
        
        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("set Admin product request"):
            response = Admin_product.send_request(data=self._payload, files=self._files)
            
        with allure.step("assert status_code = 200"):
            product_id = response.json()["data"]["product_id"]
            assert response.status_code == 200, f'{response.status_code}'
           
        with allure.step("assert product_id != None"):
            assert product_id != None, f'{product_id}'

        with allure.step(f'select db by id: {product_id}'):
            query_string = ("SELECT * FROM stylish_backend.product\
                            LEFT JOIN stylish_backend.variant\
                            ON stylish_backend.product.id = stylish_backend.variant.product_id\
                            WHERE stylish_backend.product.id=%s;")
            query_data = (product_id,)
            db.execute_query(query_string, query_data)
            db_result = db.fetchone_result()
            db.commit_query()
        
        with allure.step(f'assert db data = request_payload '):
            # 驗證商品資訊
            assert db_result["wash"] == self._payload["wash"], f'{db_result["wash"]}'
            assert db_result["note"] == self._payload["note"], f'{db_result["note"]}'
            assert db_result["place"] == self._payload["place"], f'{db_result["place"]}'
            assert db_result["story"] == self._payload["story"], f'{db_result["story"]}'
            assert db_result["title"] == self._payload["title"], f'{db_result["title"]}'
            assert db_result["size"] == self._payload["sizes"], f'{db_result["size"]}'
            assert db_result["price"] == int(self._payload["price"]), f'{db_result["price"]}'
            assert db_result["texture"] == self._payload["texture"], f'{db_result["texture"]}'
            assert db_result["category"] == self._payload["category"], f'{db_result["category"]}'
            assert db_result["color_id"] == int(self._payload["color_ids"]), f'{db_result["color_id"]}'
            assert db_result["description"] == self._payload["description"], f'{db_result["description"]}'
                
        with allure.step(f'delete product: {product_id}'):
            delete_product = DeleteAdminProductAPI(session, product_id)
            
            delete = delete_product.send_request()
            assert delete.status_code == 200, f"{delete.status_code}"
        
        with allure.step(f'select db by id: {product_id}'):
            query_string_2 = ("SELECT * FROM stylish_backend.product\
                            WHERE stylish_backend.product.id=%s;")
            query_data_2 = (product_id,)
            db.execute_query(query_string_2, query_data_2)
            db_result = db.fetchall_result()
            db.commit_query()
        
        with allure.step(f'assert db data total = 0 '):
            # 驗證刪除成功，筆數 = 0
            assert len(db_result) == 0, f'{len(db_result)}'

    def test_Admin_product_without_token(self, session):
        Admin_product = AdminProductAPI(session)
   
        with allure.step("send Admin product request"):
            response = Admin_product.send_request(data=self._payload, files=self._files)
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 401, f'{response.status_code}'
        
        with allure.step("assert status_code = 401"):
            error_msg = response.json()["errorMsg"]
            assert response.status_code == 401, f'{response.status_code}'  
            assert error_msg == "Unauthorized", f'{error_msg}'