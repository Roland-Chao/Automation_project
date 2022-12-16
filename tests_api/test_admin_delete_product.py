import pytest, allure, json, os, requests
from api_objects.login_api import LoginAPI
from page_objects.database_utils import DatabaseUtils
from api_objects.admin_product_api import AdminProductAPI
from test_data.get_data_from_excel import GetDataFromExcel
from api_objects.admin_delete_product_api import DeleteAdminProductAPI

class TestDeleteAdminProductAPI:
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
        'color_ids': ['2'], 
        'sizes': ['S'], 
        'story': 'Story Content'
    }
    
    def test_delete_admin_product_success(self, session, login_info):
        login = LoginAPI(session)
        admin_product = AdminProductAPI(session)
        db = DatabaseUtils()
        
        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
            
        with allure.step("set Admin product request"):
            response = admin_product.send_request(data=self._payload, files=self._files)
            
        with allure.step("assert status_code = 200"):
            product_id = response.json()["data"]["product_id"]
            assert response.status_code == 200, f'{response.status_code}'
           
        with allure.step("assert product_id != None"):
            assert product_id != None, f'{product_id}'

        with allure.step(f'select db by id: {product_id}'):
            query_string = ("SELECT * FROM stylish_backend.product WHERE id=%s")
            query_data = (product_id,)
            db.execute_query(query_string, query_data)
            db_result = db.fetchall_result()
            db.commit_query()
        
        with allure.step(f'assert db data total = 1 '):
            # 驗證新增成功，筆數 = 1
            assert len(db_result) == 1, f'{len(db_result)}'
             
        with allure.step(f'delete product: {product_id}'):
            delete_product = DeleteAdminProductAPI(session, product_id)
            
            delete = delete_product.send_request()
            assert delete.status_code == 200, f"{delete.status_code}"
        
        with allure.step(f'select db by id: {product_id}'):
            db.execute_query(query_string, query_data)
            db_result = db.fetchall_result()
            db.commit_query()
        
        with allure.step(f'assert db data total = 0 '):
            # 驗證刪除成功，筆數 = 0
            assert len(db_result) == 0, f'{len(db_result)}'
            
    def test_Admin_delete_product_without_token(self, session):
        delete_product = DeleteAdminProductAPI(session, '12345')
   
        with allure.step("send Admin product request"):
            response = delete_product.send_request()
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 401, f'{response.status_code}'
        
        with allure.step("assert status_code = 401"):
            error_msg = response.json()["errorMsg"]
            assert response.status_code == 401, f'{response.status_code}'  
            assert error_msg == "Unauthorized", f'{error_msg}'
    
    def test_Admin_delete_product_without_token(self, session):
        delete_product = DeleteAdminProductAPI(session, '12345')
   
        with allure.step("send Admin product request"):
            response = delete_product.send_request()
            
        with allure.step("assert status_code = 400"):
            assert response.status_code == 401, f'{response.status_code}'
        
        with allure.step("assert status_code = 401"):
            error_msg = response.json()["errorMsg"]
            assert response.status_code == 401, f'{response.status_code}'  
            assert error_msg == "Unauthorized", f'{error_msg}'

    def test_Admin_delete_product_with_invaild_id(self, session, login_info):
        login = LoginAPI(session)
        delete_product = DeleteAdminProductAPI(session, '12345')
        
        with allure.step("get login token"):
            login.set_login_token_to_session(login_info)
             
        with allure.step(f'send request'):
            response = delete_product.send_request()
            assert response.status_code == 400, f"{response.status_code}"
        
        with allure.step("assert status_code = 400"):
            error_msg = response.json()["errorMsg"]
            assert response.status_code == 400, f'{response.status_code}'  
            assert error_msg == "Product ID not found.", f'{error_msg}'