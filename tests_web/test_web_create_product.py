import allure, os, pytest
from dotenv import load_dotenv
from page_objects.action_utils import ActionUtils
from page_objects.login_page import LoginPage
from page_objects.admin_page import AdminPage
from test_data.get_data_from_excel import GetDataFromExcel

class TestCreateProduct:
    load_dotenv()
    url = os.getenv("DOMAIN")
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)
    
    @pytest.mark.parametrize('test_data', data.create_test_data("Create Product Success"))
    def test_create_product(self, browser, test_data, worker_id):
        login_page = LoginPage(browser)
        browser_action = ActionUtils(browser)
        Admin_page = AdminPage(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step("開啟 STYLISH 登入頁..."):
            browser.get(f'{self.url}/login.html')
            
        with allure.step("輸入帳密登入"): 
            login_page.stylish_login(login_info["account"], login_info["password"])
        
        with allure.step("驗證 alert 是否登入成功"): 
            browser_action.get_alert()            
            assert browser_action.get_alert().text == "Login Success", f'{browser_action.get_alert().text}'
        
        with allure.step("關閉 alert 彈窗"):  
            browser_action.get_alert().accept()
            
        with allure.step("前往後台管理頁"):  
            browser.get(f'{self.url}/admin/products.html')

        with allure.step("點選新增商品 btn"):
            Admin_page.go_to_create_product_page()
            browser_action.switch_to_window(-1)
            
        with allure.step("新增商品"): 
            Admin_page.create_new_product(test_data)
            
        with allure.step("驗證彈窗文案: "): 
            browser_action.get_alert()
            assert browser_action.get_alert().text == "Create Product Success", f'{browser_action.get_alert().text}'
            
        with allure.step("關閉彈窗"):
            browser_action.get_alert().accept()

        with allure.step("切回商品管理頁、重新整理頁面"):
            browser_action.switch_to_window(0)
            browser_action.refresh_page()

        with allure.step("驗證商品是否新增成功"):
            result1 = Admin_page.find_product_by_title()
            assert test_data["Title"] in result1, f'{result1}'
            
        with allure.step(f'前往後台管理頁 刪除商品:{test_data["Title"]}'):  
            browser.get(f'{self.url}/admin/products.html')
            Admin_page.delete_product(test_data["Title"])
            
        with allure.step(f'驗證 pop up 文案 = Delete Product Success'): 
            browser_action.get_alert()
            assert browser_action.get_alert().text == "Delete Product Success", f'{browser_action.get_alert().text}'
            
        with allure.step("關閉彈窗"):
            browser_action.get_alert().accept()
            
        with allure.step(f'驗證商品:{test_data["Title"]}已刪除成功'):
            result2 = Admin_page.find_product_by_title()
            assert test_data["Title"] not in result2, f'{result2}'
            
    @pytest.mark.parametrize('test_data', data.create_test_data("Create Product Failed"))
    def test_create_product_with_invalid_value(self, browser, test_data, worker_id):
        login_page = LoginPage(browser)
        browser_action = ActionUtils(browser)
        Admin_page = AdminPage(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step("開啟 STYLISH 登入頁..."):
            browser.get(f'{self.url}/login.html')
            
        with allure.step("輸入帳密登入"): 
            login_page.stylish_login(login_info["account"], login_info["password"])
        
        with allure.step("驗證 alert 是否登入成功"): 
            browser_action.get_alert()            
            assert browser_action.get_alert().text == "Login Success", f'{browser_action.get_alert().text}'
        
        with allure.step("關閉 alert 彈窗"):  
            browser_action.get_alert().accept()
            
        with allure.step("前往後台管理頁"):  
            browser.get(f'{self.url}/admin/products.html')

        with allure.step("點選新增商品 btn"):
            Admin_page.go_to_create_product_page()
            browser_action.switch_to_window(-1)
            
        with allure.step("新增商品"): 
            try:
                with allure.step(f'驗證彈窗文案:{test_data["Alert Msg"]}'):
                    Admin_page.create_new_product(test_data)
                    # 防呆流程，如果商品不小心新增成功，則走刪除流程還原 
                    browser_action.get_alert()
                    assert browser_action.get_alert().text == test_data["Alert Msg"], f'{browser_action.get_alert().text}'
                with allure.step(f'關閉彈窗'):
                    browser_action.get_alert().accept()
                    
            except AssertionError:
                with allure.step(f'關閉彈窗，切換回商品列表頁、重整頁面'):
                    browser_action.get_alert().accept()
                    browser_action.switch_to_window(0)
                    browser_action.refresh_page()
                    
                with allure.step(f'刪除測試失敗的商品'):
                    Admin_page.delete_product(test_data["Title"])
                    assert browser_action.get_alert().text == "Delete Product Success", f'{browser_action.get_alert().text}'
                
                with allure.step(f'關閉彈窗'):
                    browser_action.get_alert().accept()
                    
                with allure.step(f'驗證商品:{test_data["Title"]}已刪除成功'):
                    result = Admin_page.find_product_by_title()
                    assert test_data["Title"] not in result, f'{result}'
                
                raise AssertionError(f"測試失敗，商品資料為：{test_data}")
      
    def test_create_product_without_login(self, browser):
        browser_action = ActionUtils(browser)
        Admin_page = AdminPage(browser)
        # 讀取excel一筆成功的資料
        test_data = self.data.create_test_data("Create Product Failed")[0]
        
        with allure.step("開啟 STYLISH 新增商品頁..."):
            browser.get(f'{self.url}/admin/product_create.html')
            
        with allure.step("新增商品"): 
            Admin_page.create_new_product(test_data)
            
        with allure.step(f'驗證彈窗文案: Please Login First'): 
            browser_action.get_alert()
            assert browser_action.get_alert().text == "Please Login First", f'{browser_action.get_alert().text}'
            
        with allure.step("關閉彈窗"):
            browser_action.get_alert().accept()
            
        with allure.step('驗證 url 導回 login page'):
            current_url = f'{self.url}/login.html'
            assert browser.current_url == current_url, f'{browser.current_url}'